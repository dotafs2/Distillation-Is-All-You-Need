[**中文**](README_CN.md) | English

# Distillation Is All You Need

> **Distill everything. Simulate N times. Monte Carlo the possibilities.**

Take any raw human data — chat logs, diaries, voice memos — distill it into a persona, then run thousands of Monte Carlo simulations to answer questions that don't have answers yet.

## How It Works

```
Raw Data                    Persona                     Monte Carlo

 WeChat messages             Claude API distills        N parallel timelines
                              each person into a
 Diaries / notes              behavioral model           Branching at every
                                                         decision point
 Voice memos                 Captures:
                              - communication style      → P(outcome)
                              - decision patterns        → probability distribution
                              - emotional triggers
         ──────────→              ──────────→              ──────────→
```

## Quick Start

### Step 0: Clone

```bash
git clone https://github.com/dotafs2/Distillation-Is-All-You-Need.git
cd Distillation-Is-All-You-Need
```

### Step 1: Setup (any terminal)

```bash
python pipeline/setup.py
```

Downloads wx_key (WeChat 4.x key extractor) and installs Python deps (pycryptodome, zstandard, uiautomation, pywin32, etc.).

### Step 2: Decrypt (admin terminal, run once)

```bash
python pipeline/decrypt_wx4.py
```

Requires **admin privileges** (reads WeChat process memory). WeChat must be running and logged in. Auto-detects wxid, extracts 16 per-DB encryption keys, decrypts all databases.

Use `--wxid wxid_xxx` to target a specific account. Use `--keys-only` to extract keys without decrypting.

### Step 3: Read messages (any terminal)

```bash
python pipeline/read_wx_msg.py              # Latest 10 messages
python pipeline/read_wx_msg.py --last 20    # Latest 20
python pipeline/read_wx_msg.py --watch      # Live polling (every 3s)
```

No admin needed — uses saved keys from Step 2.

### Step 4: Send messages (normal terminal, WeChat visible on screen)

```bash
python pipeline/send_wx_msg.py --to "CONTACT_NAME" --msg "hello"
python pipeline/send_wx_msg.py --to "CONTACT_NAME" --msg "line1" --msg "line2"
```

Uses Windows UI Automation (not hooks, no ban risk). Don't touch mouse/keyboard for a few seconds while it runs.

## Project Structure

```
Distillation-Is-All-You-Need/
├── pipeline/                # Data pipeline
│   ├── setup.py             #   One-command env setup
│   ├── decrypt_wx4.py       #   WeChat 4.x DB decryption (admin, run once)
│   ├── read_wx_msg.py       #   Read/poll messages from encrypted DB
│   └── send_wx_msg.py       #   Send messages via UI Automation
├── simulator/               # Monte Carlo simulator (WIP)
├── third_party/             # Vendored dependencies
│   ├── WeChatMsg/           #   WeChat 3.x export tool
│   ├── wechat-decrypt/      #   WeChat 4.x SQLCipher 4 decryptor
│   └── WeChatMassTool/      #   WeChat message sender (UI Automation)
└── README.md
```

## The Pipeline

```
Step 1: Decrypt                    Step 2: Distill                 Step 3: Simulate

WeChat 4.x encrypted DB     →     Extract persona via LLM    →   Monte Carlo N runs

 ┌─ message_0.db ─┐                ┌─ persona A ─┐                ┌─ timeline 1 ─┐
 │  contact.db     │         →     │  persona B   │         →     │  timeline 2   │
 │  session.db     │               └──────────────┘               │  ...          │
 └─────────────────┘                                              │  timeline N   │
                                                                  └───────────────┘
                                                                        ↓
                                                                  P(X) = count(X) / N
```

## Requirements

- **OS**: Windows 10/11
- **WeChat**: 4.x (tested on 4.1.7.30)
- **Python**: 3.12+
- **Admin**: Only for Step 2 (key extraction)

## Third Party

See [third_party/README.md](third_party/README.md)
