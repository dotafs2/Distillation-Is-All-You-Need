# Third Party Dependencies

## WeChatMsg
- 来源：[yincongcyincong/wechatmsg](https://gitee.com/linrh/wechatmsg)，原作者：司小远
- 许可：GPL-3.0
- 用途：微信聊天记录解密与导出（Windows）
- 修改说明：修复 Python 3.13 兼容性，移除版本锁定的 Pillow，删除错误的 google 包，补充缺失的 pilk / lz4 / requests / protobuf 依赖
- 位置：third_party/WeChatMsg/

## wx_key
- 来源：[ycccccccy/wx_key](https://github.com/ycccccccy/wx_key)（已归档，只读）
- 版本：v2.1.8
- 许可：MIT
- 用途：获取微信 4.0+ 数据库加密密钥和图片解密密钥（通过 DLL 注入读取内存）
- 已测试版本：4.0.5.17, 4.1.0.30, 4.1.2.17, 4.1.2.18, 4.1.4.15, 4.1.4.17, 4.1.5.11
- 位置：third_party/wx_key/
- 注意：预编译 Windows 二进制，需在不含中文的路径下运行

## wechat-decrypt
- 来源：[ylytdeng/wechat-decrypt](https://github.com/ylytdeng/wechat-decrypt)
- 许可：MIT
- 用途：微信 4.x 数据库全自动解密（密钥提取 + SQLCipher 4 解密）
- 技术：从 Weixin.exe 进程内存扫描 per-DB raw key，AES-256-CBC + HMAC-SHA512 解密
- 依赖：pycryptodome, zstandard
- 位置：third_party/wechat-decrypt/
- 使用：通过 `pipeline/decrypt_wx4.py` 调用，或直接 `cd third_party/wechat-decrypt && python main.py decrypt`

## PyWxDump
- 来源：[xaoyaoo/PyWxDump](https://github.com/xaoyaoo/PyWxDump)（原库已于 2025年10月因微信律师函删库）
- PyPI 包：pip install pywxdump（截至 2026年4月仍可用，版本 3.1.46）
- 许可：原项目 MIT
- 用途：微信数据库解密，提供 wxdump ui 网页界面，读取密钥、解密 db、导出聊天记录
- 注意：原作者已停止维护，使用需自行评估合规风险
