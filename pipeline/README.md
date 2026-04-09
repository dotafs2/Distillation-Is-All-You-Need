[**中文**](README_CN.md) | English

# Pipeline

Raw data in, clean features out.

```
WeChat encrypted DB  →  decrypt_wx4.py  →  clean SQLite  →  CSV  →  simulator
```

## Scripts

| Script | What it does |
|---|---|
| `setup.py` | One-command env setup: download wx_key + install deps |
| `decrypt_wx4.py` | Auto-detect wxid, extract keys from memory, decrypt all DBs |
| `send_wx_msg.py` | Send WeChat message via UI Automation: `--to NAME --msg "text"` |
| `read_wx_msg.py` | Read/poll latest messages from encrypted DB: `--watch` for live monitoring |
