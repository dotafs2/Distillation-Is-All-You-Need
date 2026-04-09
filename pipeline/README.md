# Pipeline / 数据管线

Raw data in, clean features out. 原始数据进，干净特征出。

```
WeChat encrypted DB  →  decrypt_wx4.py  →  clean SQLite  →  CSV  →  simulator
微信加密数据库          解密                 明文数据库        导出      喂给模拟器
```

## Scripts / 脚本

| Script | What it does |
|---|---|
| `setup.py` | One-command env setup: download wx_key + install deps / 一键搭建环境 |
| `decrypt_wx4.py` | Auto-detect wxid, extract keys from memory, decrypt all DBs / 自动检测账号、提取密钥、解密全部数据库 |
