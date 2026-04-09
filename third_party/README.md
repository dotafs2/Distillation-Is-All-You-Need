# Third Party Dependencies / 第三方依赖

## WeChatMsg
- Source / 来源: [yincongcyincong/wechatmsg](https://gitee.com/linrh/wechatmsg)
- License: GPL-3.0
- Purpose: WeChat 3.x message decryption & export / 微信 3.x 聊天记录解密与导出
- Modifications / 修改: Python 3.13 compat fixes, removed Pillow version lock, added missing deps (pilk, lz4, requests, protobuf)
- Location: `third_party/WeChatMsg/`

## wx_key
- Source / 来源: [ycccccccy/wx_key](https://github.com/ycccccccy/wx_key) (archived)
- Version: v2.1.8 | License: MIT
- Purpose: Extract WeChat 4.0+ DB encryption keys via DLL injection / 通过 DLL 注入获取微信 4.0+ 数据库密钥
- Tested versions: 4.0.5.17, 4.1.0.30, 4.1.2.17, 4.1.2.18, 4.1.4.15, 4.1.4.17, 4.1.5.11
- Location: `third_party/wx_key/` (downloaded on demand via `pipeline/setup.py`, not in git)
- Note: Windows binary, path must not contain Chinese characters / 路径不能含中文

## wechat-decrypt
- Source / 来源: [ylytdeng/wechat-decrypt](https://github.com/ylytdeng/wechat-decrypt)
- License: MIT
- Purpose: Fully automated WeChat 4.x decryption (key extraction + SQLCipher 4) / 微信 4.x 全自动解密
- Tech: Memory-scan per-DB raw keys from Weixin.exe, AES-256-CBC + HMAC-SHA512
- Deps: pycryptodome, zstandard
- Location: `third_party/wechat-decrypt/`
- Usage: `python pipeline/decrypt_wx4.py` or `cd third_party/wechat-decrypt && python main.py decrypt`

## WeChatMassTool
- Source / 来源: [Frica01/WeChatMassTool](https://github.com/Frica01/WeChatMassTool)
- License: MIT
- Purpose: Send WeChat messages via Windows UI Automation (no hooks, no ban risk) / 通过 UI 自动化发送微信消息（非 hook，不封号）
- Tech: uiautomation + win32gui + clipboard
- Deps: uiautomation, pywin32, WMI, comtypes
- Location: `third_party/WeChatMassTool/`
- Usage: `python pipeline/send_wx_msg.py --to NAME --msg "text"`
- Note: WeChat 4.x config patched (window class `Qt51514QWindowIcon`, process `Weixin.exe`)

## PyWxDump
- Source / 来源: [xaoyaoo/PyWxDump](https://github.com/xaoyaoo/PyWxDump) (repo deleted Oct 2025, legal takedown)
- PyPI: `pip install pywxdump` (v3.1.46 still available as of Apr 2026)
- License: MIT (original) | Purpose: WeChat DB decryption, web UI, chat export / 微信数据库解密、网页界面、聊天记录导出
- Note: Unmaintained, use at your own risk / 原作者已停止维护
