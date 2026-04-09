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

```bash
git clone https://github.com/dotafs2/Distillation-Is-All-You-Need.git
cd Distillation-Is-All-You-Need

python pipeline/setup.py          # Install deps + download tools
python pipeline/decrypt_wx4.py    # Decrypt WeChat DB (admin terminal, WeChat 4.x running)
```

Decrypted databases land in `third_party/wechat-decrypt/decrypted/`.

## Project Structure

```
Distillation-Is-All-You-Need/
├── pipeline/                # Data pipeline
│   ├── setup.py             #   One-command env setup
│   └── decrypt_wx4.py       #   WeChat 4.x DB decryption
├── simulator/               # Monte Carlo simulator
├── third_party/             # Vendored dependencies
│   ├── WeChatMsg/           #   WeChat export tool (3.x)
│   └── wechat-decrypt/      #   WeChat 4.x SQLCipher 4 decryptor
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

## Third Party

See [third_party/README.md](third_party/README.md)
