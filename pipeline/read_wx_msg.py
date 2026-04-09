"""
读取微信最新消息（从加密数据库实时解密）

用法:
    python pipeline/read_wx_msg.py                          # 显示最新10条
    python pipeline/read_wx_msg.py --last 20                # 最新20条
    python pipeline/read_wx_msg.py --watch                  # 持续监听新消息
    python pipeline/read_wx_msg.py --watch --interval 5     # 每5秒检查一次

前提: all_keys.json 已存在（先跑过一次 decrypt_wx4.py）
"""
import argparse
import datetime
import json
import os
import sqlite3
import struct
import sys
import time

from Crypto.Cipher import AES

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WECHAT_DECRYPT_DIR = os.path.join(PROJECT_ROOT, "third_party", "wechat-decrypt")
KEYS_FILE = os.path.join(WECHAT_DECRYPT_DIR, "all_keys.json")

PAGE_SZ = 4096
RESERVE_SZ = 80
SALT_SZ = 16
SQLITE_HDR = b"SQLite format 3\x00"


def find_wxid_db_dir():
    """自动查找小号的 db_storage 目录"""
    base = os.path.join(os.environ.get("USERPROFILE", ""), "Documents", "xwechat_files")
    if not os.path.isdir(base):
        return None
    # 使用 keys 文件中保存的 db_dir
    if os.path.exists(KEYS_FILE):
        with open(KEYS_FILE, encoding="utf-8") as f:
            keys = json.load(f)
        saved = keys.get("_db_dir", "")
        if saved and os.path.isdir(saved):
            return saved
    # fallback: 找最小的 wxid（小号数据量小）
    wxids = []
    for name in os.listdir(base):
        db_storage = os.path.join(base, name, "db_storage")
        if os.path.isdir(db_storage) and name.startswith("wxid_"):
            wxids.append((name, db_storage))
    if wxids:
        return wxids[0][1]
    return None


def load_enc_key(db_rel_path="message\\message_0.db"):
    """从 all_keys.json 加载加密密钥"""
    if not os.path.exists(KEYS_FILE):
        print(f"[!] 密钥文件不存在: {KEYS_FILE}")
        print("    请先在管理员终端运行: python pipeline/decrypt_wx4.py")
        sys.exit(1)
    with open(KEYS_FILE, encoding="utf-8") as f:
        keys = json.load(f)
    # 尝试多种路径分隔符
    for variant in [db_rel_path, db_rel_path.replace("\\", "/")]:
        if variant in keys and not variant.startswith("_"):
            return bytes.fromhex(keys[variant]["enc_key"])
    print(f"[!] 找不到 {db_rel_path} 的密钥")
    sys.exit(1)


def decrypt_db_to_memory(db_path, enc_key):
    """解密数据库到临时文件并返回 sqlite3 连接"""
    with open(db_path, "rb") as f:
        db_data = f.read()

    tmp_path = db_path + ".decrypted.tmp"
    total_pages = len(db_data) // PAGE_SZ

    with open(tmp_path, "wb") as fout:
        for pgno in range(1, total_pages + 1):
            page = db_data[(pgno - 1) * PAGE_SZ : pgno * PAGE_SZ]
            iv = page[PAGE_SZ - RESERVE_SZ : PAGE_SZ - RESERVE_SZ + 16]
            if pgno == 1:
                enc = page[SALT_SZ : PAGE_SZ - RESERVE_SZ]
                dec = AES.new(enc_key, AES.MODE_CBC, iv).decrypt(enc)
                fout.write(SQLITE_HDR + dec + b"\x00" * RESERVE_SZ)
            else:
                enc = page[: PAGE_SZ - RESERVE_SZ]
                dec = AES.new(enc_key, AES.MODE_CBC, iv).decrypt(enc)
                fout.write(dec + b"\x00" * RESERVE_SZ)

    with open(tmp_path, "r+b") as f:
        f.seek(20)
        f.write(struct.pack("B", RESERVE_SZ))
        f.seek(28)
        f.write(struct.pack(">I", total_pages))

    conn = sqlite3.connect(tmp_path)
    return conn, tmp_path


def get_messages(conn, limit=10):
    """从解密的数据库中提取消息"""
    messages = []
    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()
    for (table_name,) in tables:
        if "Msg_" not in table_name:
            continue
        rows = conn.execute(
            f"SELECT create_time, message_content, local_type "
            f"FROM [{table_name}] ORDER BY create_time DESC LIMIT ?",
            (limit,),
        ).fetchall()
        for ts, content, msg_type in reversed(rows):
            if not ts:
                continue
            if isinstance(content, bytes):
                content = content.decode("utf-8", errors="replace")
            messages.append(
                {
                    "time": datetime.datetime.fromtimestamp(ts),
                    "content": content or "",
                    "type": msg_type,
                }
            )
    messages.sort(key=lambda m: m["time"])
    return messages[-limit:]


def format_message(msg):
    """格式化单条消息"""
    ts = msg["time"].strftime("%Y-%m-%d %H:%M:%S")
    if msg["type"] == 10000:
        return f"  [{ts}] [system] {msg['content']}"
    elif msg["type"] == 1:
        return f"  [{ts}] {msg['content']}"
    else:
        return f"  [{ts}] [type={msg['type']}] {msg['content'][:50]}"


def read_latest(db_dir, enc_key, limit=10):
    """读取最新消息"""
    msg_db_path = os.path.join(db_dir, "message", "message_0.db")
    if not os.path.exists(msg_db_path):
        print(f"[!] 数据库不存在: {msg_db_path}")
        return []

    conn, tmp = decrypt_db_to_memory(msg_db_path, enc_key)
    try:
        messages = get_messages(conn, limit)
    finally:
        conn.close()
        try:
            os.remove(tmp)
        except OSError:
            pass
    return messages


def main():
    parser = argparse.ArgumentParser(description="Read latest WeChat messages")
    parser.add_argument("--last", type=int, default=10, help="Number of messages")
    parser.add_argument("--watch", action="store_true", help="Continuously poll")
    parser.add_argument("--interval", type=float, default=3, help="Poll interval (seconds)")
    args = parser.parse_args()

    db_dir = find_wxid_db_dir()
    if not db_dir:
        print("[!] 找不到微信数据目录")
        sys.exit(1)

    enc_key = load_enc_key()
    print(f"[+] 数据目录: {db_dir}")

    if not args.watch:
        messages = read_latest(db_dir, enc_key, args.last)
        print(f"\n最新 {len(messages)} 条消息:")
        for msg in messages:
            print(format_message(msg))
    else:
        print(f"[*] 监听模式 (每 {args.interval}s 检查一次, Ctrl+C 停止)\n")
        seen = set()
        while True:
            try:
                messages = read_latest(db_dir, enc_key, args.last)
                for msg in messages:
                    key = (msg["time"], msg["content"])
                    if key not in seen:
                        seen.add(key)
                        print(format_message(msg))
                        sys.stdout.flush()
                time.sleep(args.interval)
            except KeyboardInterrupt:
                print("\n[*] Stopped.")
                break


if __name__ == "__main__":
    main()
