"""
WeChat 4.x 数据库解密 pipeline

用法:
    python pipeline/decrypt_wx4.py                  # 自动检测 wxid, 提取密钥, 解密
    python pipeline/decrypt_wx4.py --wxid wxid_xxx  # 指定 wxid
    python pipeline/decrypt_wx4.py --list            # 列出所有可用 wxid
"""
import argparse
import glob
import json
import os
import sys

# ── 路径设置 ──────────────────────────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WECHAT_DECRYPT_DIR = os.path.join(PROJECT_ROOT, "third_party", "wechat-decrypt")
WX_KEY_DIR = os.path.join(PROJECT_ROOT, "third_party", "wx_key")

# 将 wechat-decrypt 加入 sys.path（它的 import 使用相对路径）
sys.path.insert(0, WECHAT_DECRYPT_DIR)


def find_xwechat_root():
    """查找 xwechat_files 所在目录"""
    user_profile = os.environ.get("USERPROFILE", "")
    candidates = [
        os.path.join(user_profile, "Documents", "xwechat_files"),
    ]
    # 也检查微信 ini 配置
    appdata = os.environ.get("APPDATA", "")
    config_dir = os.path.join(appdata, "Tencent", "xwechat", "config")
    if os.path.isdir(config_dir):
        for ini_file in glob.glob(os.path.join(config_dir, "*.ini")):
            try:
                with open(ini_file, "r", encoding="utf-8") as f:
                    content = f.read(1024).strip()
                if content and os.path.isdir(content):
                    xwechat = os.path.join(content, "xwechat_files")
                    if os.path.isdir(xwechat):
                        candidates.append(xwechat)
            except (OSError, UnicodeDecodeError):
                continue
    for c in candidates:
        if os.path.isdir(c):
            return c
    return None


def list_wxids(xwechat_root):
    """列出所有 wxid 目录及其 db_storage 大小"""
    wxids = []
    for name in os.listdir(xwechat_root):
        full = os.path.join(xwechat_root, name)
        db_storage = os.path.join(full, "db_storage")
        if os.path.isdir(db_storage) and name.startswith("wxid_"):
            # 计算 db_storage 总大小
            total = 0
            for root, dirs, files in os.walk(db_storage):
                for f in files:
                    if f.endswith(".db"):
                        total += os.path.getsize(os.path.join(root, f))
            wxids.append((name, total))
    wxids.sort(key=lambda x: x[1], reverse=True)
    return wxids


def choose_wxid(xwechat_root):
    """交互式选择 wxid"""
    wxids = list_wxids(xwechat_root)
    if not wxids:
        print("[!] 未找到任何 wxid 目录")
        sys.exit(1)
    if len(wxids) == 1:
        print(f"[+] 仅找到一个账号: {wxids[0][0]}")
        return wxids[0][0]

    print("[?] 检测到多个微信账号:")
    for i, (wxid, size) in enumerate(wxids, 1):
        print(f"    {i}. {wxid} ({size / 1024 / 1024:.1f} MB)")
    while True:
        try:
            choice = input(f"请选择 [1-{len(wxids)}]: ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(wxids):
                return wxids[idx][0]
        except (ValueError, EOFError, KeyboardInterrupt):
            print()
            sys.exit(1)
        print("    无效输入，请重新选择")


def write_config(db_dir):
    """写入 wechat-decrypt 的 config.json"""
    config_path = os.path.join(WECHAT_DECRYPT_DIR, "config.json")
    config = {
        "db_dir": db_dir,
        "keys_file": os.path.join(WECHAT_DECRYPT_DIR, "all_keys.json"),
        "decrypted_dir": os.path.join(WECHAT_DECRYPT_DIR, "decrypted"),
        "decoded_image_dir": os.path.join(WECHAT_DECRYPT_DIR, "decoded_images"),
        "wechat_process": "Weixin.exe",
    }
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    print(f"[+] 配置已写入: {config_path}")
    return config


def check_wechat_running():
    """检查微信是否在运行"""
    import subprocess
    r = subprocess.run(
        ["tasklist.exe", "/FI", "IMAGENAME eq Weixin.exe", "/FO", "CSV", "/NH"],
        capture_output=True, text=True
    )
    return "Weixin.exe" in r.stdout


def extract_keys(config):
    """从微信进程内存中提取数据库密钥"""
    keys_file = config["keys_file"]

    # 检查是否已有密钥
    if os.path.exists(keys_file):
        try:
            with open(keys_file, encoding="utf-8") as f:
                keys = json.load(f)
            saved_dir = keys.get("_db_dir", "")
            if os.path.normcase(os.path.normpath(saved_dir)) == os.path.normcase(
                os.path.normpath(config["db_dir"])
            ):
                count = sum(1 for k in keys if not k.startswith("_"))
                if count > 0:
                    print(f"[+] 已有 {count} 个密钥 (来自上次提取)")
                    reuse = input("    是否复用? [Y/n]: ").strip().lower()
                    if reuse != "n":
                        return
        except (json.JSONDecodeError, ValueError):
            pass

    print("[*] 正在从微信进程内存提取密钥...")
    print("    (需要微信正在运行且已登录)")
    print()

    # 切换工作目录到 wechat-decrypt 以保证其 import 正常
    old_cwd = os.getcwd()
    os.chdir(WECHAT_DECRYPT_DIR)
    try:
        from find_all_keys import main as do_extract
        do_extract()
    finally:
        os.chdir(old_cwd)

    if not os.path.exists(keys_file):
        print("[!] 密钥提取失败")
        sys.exit(1)


def decrypt_databases(config):
    """解密所有数据库"""
    print()
    print("[*] 开始解密数据库...")
    print()

    old_cwd = os.getcwd()
    os.chdir(WECHAT_DECRYPT_DIR)
    try:
        from decrypt_db import main as do_decrypt
        do_decrypt()
    finally:
        os.chdir(old_cwd)


def main():
    parser = argparse.ArgumentParser(description="WeChat 4.x 数据库解密 pipeline")
    parser.add_argument("--wxid", type=str, help="指定 wxid（如 wxid_xxx_xxxx）")
    parser.add_argument("--list", action="store_true", help="列出所有可用 wxid")
    parser.add_argument("--keys-only", action="store_true", help="只提取密钥，不解密")
    args = parser.parse_args()

    print("=" * 60)
    print("  WeChat 4.x 数据库解密 Pipeline")
    print("=" * 60)
    print()

    # 1. 查找 xwechat_files
    xwechat_root = find_xwechat_root()
    if not xwechat_root:
        print("[!] 未找到微信数据目录 (xwechat_files)")
        print("    请确认微信 4.x 已安装并至少登录过一次")
        sys.exit(1)
    print(f"[+] 微信数据目录: {xwechat_root}")

    # 2. 列出或选择 wxid
    if args.list:
        wxids = list_wxids(xwechat_root)
        for wxid, size in wxids:
            print(f"  {wxid}  ({size / 1024 / 1024:.1f} MB)")
        return

    wxid = args.wxid or choose_wxid(xwechat_root)
    db_dir = os.path.join(xwechat_root, wxid, "db_storage")
    if not os.path.isdir(db_dir):
        print(f"[!] db_storage 不存在: {db_dir}")
        sys.exit(1)
    print(f"[+] 目标账号: {wxid}")
    print(f"[+] db_storage: {db_dir}")

    # 3. 检查微信进程
    if not check_wechat_running():
        print()
        print("[!] 微信未运行! 请先启动微信并登录, 然后重新运行此脚本")
        print("    (提取密钥需要从运行中的微信进程内存读取)")
        sys.exit(1)
    print("[+] 微信进程运行中 (Weixin.exe)")

    # 4. 写入配置
    config = write_config(db_dir)
    print()

    # 5. 提取密钥
    extract_keys(config)

    if args.keys_only:
        print("\n[+] 密钥提取完成 (--keys-only)")
        return

    # 6. 解密数据库
    decrypt_databases(config)

    # 7. 完成
    decrypted_dir = config["decrypted_dir"]
    print()
    print("=" * 60)
    print("  解密完成!")
    print("=" * 60)
    print(f"  解密后的数据库在: {decrypted_dir}")
    print()
    print("  后续步骤:")
    print("    1. 可用 SQLite 浏览器直接查看 message_0.db, contact.db 等")
    print("    2. 或运行 wechat-decrypt 的 Web UI:")
    print(f"       cd {WECHAT_DECRYPT_DIR} && python main.py")
    print()


if __name__ == "__main__":
    main()
