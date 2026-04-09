中文 | [**English**](README.md)

# 数据管线

原始数据进，干净特征出。

```
微信加密数据库  →  decrypt_wx4.py  →  明文数据库  →  CSV  →  喂给模拟器
```

## 脚本

| 脚本 | 功能 |
|---|---|
| `setup.py` | 一键搭建环境：下载 wx_key + 安装依赖 |
| `decrypt_wx4.py` | 自动检测账号、提取密钥、解密全部数据库 |
| `send_wx_msg.py` | 通过 UI 自动化发送微信消息：`--to 联系人 --msg "内容"` |
