"""
一键环境搭建

用法 (普通终端即可):
    python pipeline/setup.py

完成后:
    1. 以管理员身份打开终端
    2. python pipeline/decrypt_wx4.py
"""
import os
import subprocess
import sys
import urllib.request
import zipfile

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WX_KEY_DIR = os.path.join(PROJECT_ROOT, "third_party", "wx_key")
WX_KEY_ZIP_URL = (
    "https://github.com/ycccccccy/wx_key/releases/download/v2.1.8/"
    "wx_key-windows-v2.1.8.zip"
)


def install_deps():
    """安装 Python 依赖"""
    print("[1/2] 安装 Python 依赖...")
    deps = ["pycryptodome", "zstandard"]
    # WeChatMsg 的依赖 (可选, 用于 web UI)
    # deps += ["flask", "pyecharts", "PyQt5", ...]
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--quiet"] + deps
    )
    print("  OK")


def download_wx_key():
    """下载并解压 wx_key"""
    if os.path.exists(os.path.join(WX_KEY_DIR, "wx_key.exe")):
        print("[2/2] wx_key 已存在，跳过下载")
        return

    print("[2/2] 下载 wx_key v2.1.8 (~49MB)...")
    os.makedirs(WX_KEY_DIR, exist_ok=True)
    zip_path = os.path.join(WX_KEY_DIR, "wx_key.zip")

    urllib.request.urlretrieve(WX_KEY_ZIP_URL, zip_path)
    print("  下载完成，解压中...")

    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(WX_KEY_DIR)
    os.remove(zip_path)
    print("  OK")


def main():
    print("=" * 60)
    print("  Distillation-Is-All-You-Need 环境搭建")
    print("=" * 60)
    print()

    install_deps()
    download_wx_key()

    print()
    print("=" * 60)
    print("  搭建完成!")
    print("=" * 60)
    print()
    print("  下一步 (需要管理员权限):")
    print()
    print("    python pipeline/decrypt_wx4.py")
    print()
    print("  这会自动:")
    print("    1. 检测本机微信账号")
    print("    2. 从微信进程内存提取数据库密钥")
    print("    3. 解密所有聊天数据库")
    print()
    print("  前提: 微信 4.x 已登录且正在运行")
    print()


if __name__ == "__main__":
    main()
