# Third Party Dependencies

## WeChatMsg
- 来源：[yincongcyincong/wechatmsg](https://gitee.com/linrh/wechatmsg)，原作者：司小远
- 许可：GPL-3.0
- 用途：微信聊天记录解密与导出（Windows）
- 修改说明：修复 Python 3.13 兼容性，移除版本锁定的 Pillow，删除错误的 google 包，补充缺失的 pilk / lz4 / requests / protobuf 依赖
- 位置：third_party/WeChatMsg/

## PyWxDump
- 来源：[xaoyaoo/PyWxDump](https://github.com/xaoyaoo/PyWxDump)（原库已于 2025年10月因微信律师函删库）
- PyPI 包：pip install pywxdump（截至 2026年4月仍可用，版本 3.1.46）
- 许可：原项目 MIT
- 用途：微信数据库解密，提供 wxdump ui 网页界面，读取密钥、解密 db、导出聊天记录
- 注意：原作者已停止维护，使用需自行评估合规风险
