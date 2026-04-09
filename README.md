# Distillation Is All You Need

> **Distill everything. Simulate N times. Monte Carlo the possibilities.**
>
> 蒸馏一切。模拟 N 次。蒙特卡洛出所有可能性。

Take any raw human data — chat logs, diaries, voice memos — distill it into a persona, then run thousands of Monte Carlo simulations to answer questions that don't have answers yet.

用任何真实人类数据 — 聊天记录、日记、语音备忘 — 蒸馏成 persona，然后跑上千次蒙特卡洛模拟，回答那些还没有答案的问题。

## How It Works / 工作原理

```
Raw Data                    Persona                     Monte Carlo
原始数据                     人格蒸馏                      蒙特卡洛模拟

 WeChat messages             Claude API distills        N parallel timelines
 微信聊天记录                  each person into a          N 条平行时间线
                              behavioral model
 Diaries / notes              蒸馏出行为模型               Branching at every
 日记 / 笔记                                              decision point
                             Captures:                    在每个决策点分叉
 Voice memos                  - communication style
 语音备忘                      - decision patterns         → P(outcome)
                              - emotional triggers         → 结果概率分布
         ──────────→              ──────────→              ──────────→
```

## Quick Start / 快速开始

```bash
git clone https://github.com/dotafs2/Distillation-Is-All-You-Need.git
cd Distillation-Is-All-You-Need

python pipeline/setup.py          # Install deps + download tools / 安装依赖 + 下载工具
python pipeline/decrypt_wx4.py    # Decrypt WeChat DB (admin terminal, WeChat 4.x running)
                                  # 解密微信数据库（管理员终端，微信 4.x 需运行中）
```

Decrypted databases land in `third_party/wechat-decrypt/decrypted/`.

## Project Structure / 项目结构

```
Distillation-Is-All-You-Need/
├── pipeline/                # Data pipeline / 数据管线
│   ├── setup.py             #   One-command setup / 一键搭建
│   └── decrypt_wx4.py       #   WeChat 4.x DB decryption / 微信数据库解密
├── simulator/               # Monte Carlo simulator / 蒙特卡洛模拟器
├── third_party/             # Vendored dependencies / 第三方依赖
│   ├── WeChatMsg/           #   WeChat export tool (3.x)
│   └── wechat-decrypt/      #   WeChat 4.x SQLCipher 4 decryptor
└── README.md
```

## The Pipeline / 数据管线

```
Step 1: Decrypt                    Step 2: Distill                 Step 3: Simulate
解密                                蒸馏                             模拟

WeChat 4.x encrypted DB     →     Extract persona via LLM    →   Monte Carlo N runs
微信加密数据库                       通过 LLM 提取人格                 蒙特卡洛 N 次模拟

 ┌─ message_0.db ─┐                ┌─ persona A ─┐                ┌─ timeline 1 ─┐
 │  contact.db     │         →     │  persona B   │         →     │  timeline 2   │
 │  session.db     │               └──────────────┘               │  ...          │
 └─────────────────┘                                              │  timeline N   │
                                                                  └───────────────┘
                                                                        ↓
                                                                  P(X) = count(X) / N
```

## Third Party / 第三方依赖

See [third_party/README.md](third_party/README.md)
