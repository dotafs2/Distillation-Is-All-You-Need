"""
通过键盘模拟发送微信消息（微信 4.x 兼容）

用法:
    python pipeline/send_wx_msg.py --to DOTAFS --msg "hello from pipeline"
    python pipeline/send_wx_msg.py --to DOTAFS --msg "line1" --msg "line2"

前提: 微信已登录且窗口存在
"""
import argparse
import time
import win32gui
import win32con
import win32api
import uiautomation as auto


WECHAT_CLASSNAME = "Qt51514QWindowIcon"
WECHAT_TITLE = "Weixin"


def find_wechat_window():
    """找到微信主窗口"""
    hwnd = win32gui.FindWindow(WECHAT_CLASSNAME, WECHAT_TITLE)
    if not hwnd:
        # fallback: 遍历所有窗口
        result = []
        def callback(h, _):
            if win32gui.GetClassName(h) == WECHAT_CLASSNAME:
                result.append(h)
            return True
        win32gui.EnumWindows(callback, None)
        if result:
            hwnd = result[0]
    return hwnd


def bring_to_front(hwnd):
    """把窗口带到前台"""
    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    # Shell 的 SetForegroundWindow 有限制，用 AttachThreadInput 绕过
    import ctypes
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    current_thread = kernel32.GetCurrentThreadId()
    target_thread = user32.GetWindowThreadProcessId(hwnd, None)
    if current_thread != target_thread:
        user32.AttachThreadInput(current_thread, target_thread, True)
    user32.SetForegroundWindow(hwnd)
    if current_thread != target_thread:
        user32.AttachThreadInput(current_thread, target_thread, False)
    time.sleep(0.5)


def send_message(contact_name, messages):
    """
    发送消息给指定联系人

    流程: Ctrl+F 搜索 → 粘贴联系人名 → Enter 选中 → 输入消息 → Enter 发送
    """
    hwnd = find_wechat_window()
    if not hwnd:
        print("[!] 找不到微信窗口")
        print("    确认微信已登录且没有完全最小化到托盘")
        return False

    print(f"[+] 找到微信窗口: hwnd={hwnd}")
    bring_to_front(hwnd)
    time.sleep(0.3)

    # Ctrl+F 打开搜索
    print("[*] Opening search...")
    auto.SendKeys("{Ctrl}f")
    time.sleep(0.5)

    # 清空搜索框 + 输入联系人名
    auto.SendKeys("{Ctrl}a")
    time.sleep(0.1)
    auto.SetClipboardText(contact_name)
    auto.SendKeys("{Ctrl}v")
    print(f"[*] Searching for '{contact_name}'...")
    time.sleep(1.5)  # 等搜索结果加载

    # Enter 选中第一个搜索结果
    print("[*] Selecting first result...")
    auto.SendKeys("{Enter}")
    time.sleep(1.0)  # 等聊天窗口完全加载

    # 点击聊天输入框区域（窗口底部中间位置）
    rect = win32gui.GetWindowRect(hwnd)
    win_w = rect[2] - rect[0]
    win_h = rect[3] - rect[1]
    # 输入框大约在窗口底部 15% 区域的中间
    click_x = rect[0] + int(win_w * 0.6)
    click_y = rect[3] - int(win_h * 0.08)
    print(f"[*] Clicking input area at ({click_x}, {click_y})...")
    win32api.SetCursorPos((click_x, click_y))
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(0.3)

    # 发送每条消息
    for msg in messages:
        print(f"[*] Sending: {msg}")
        auto.SetClipboardText(msg)
        time.sleep(0.1)
        auto.SendKeys("{Ctrl}v")
        time.sleep(0.3)
        auto.SendKeys("{Enter}")
        time.sleep(0.5)

    print("[+] Done!")
    return True


def main():
    parser = argparse.ArgumentParser(description="Send WeChat message (WeChat 4.x)")
    parser.add_argument("--to", required=True, help="Contact name / 联系人名称")
    parser.add_argument("--msg", action="append", required=True, help="Message (repeatable) / 消息")
    args = parser.parse_args()

    print(f"[*] Target: {args.to}")
    print(f"[*] Messages: {args.msg}")
    send_message(args.to, args.msg)


if __name__ == "__main__":
    main()
