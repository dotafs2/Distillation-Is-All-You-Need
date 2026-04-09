中文 | [**English**](README.md)

# Distillation Is All You Need

> **蒸馏一切。模拟 N 次。蒙特卡洛出所有可能性。**

用任何真实人类数据 — 聊天记录、日记、语音备忘 — 蒸馏成 persona，然后跑上千次蒙特卡洛模拟，回答那些还没有答案的问题。

## 工作原理

```
原始数据                     人格蒸馏                      蒙特卡洛模拟

 微信聊天记录                  Claude API 将每个人            N 条平行时间线
                              蒸馏为行为模型
 日记 / 笔记                                               在每个决策点分叉
                             提取:
 语音备忘                      - 沟通风格                    → P(结果)
                              - 决策模式                    → 概率分布
                              - 情绪触发点
         ──────────→              ──────────→              ──────────→
```

## 快速开始

```bash
git clone https://github.com/dotafs2/Distillation-Is-All-You-Need.git
cd Distillation-Is-All-You-Need

python pipeline/setup.py          # 安装依赖 + 下载工具
python pipeline/decrypt_wx4.py    # 解密微信数据库（需管理员终端，微信 4.x 需运行中）
```

解密后的数据库在 `third_party/wechat-decrypt/decrypted/`。

## 项目结构

```
Distillation-Is-All-You-Need/
├── pipeline/                # 数据管线
│   ├── setup.py             #   一键环境搭建
│   └── decrypt_wx4.py       #   微信 4.x 数据库解密
├── simulator/               # 蒙特卡洛模拟器
├── third_party/             # 第三方依赖
│   ├── WeChatMsg/           #   微信聊天记录导出工具 (3.x)
│   └── wechat-decrypt/      #   微信 4.x SQLCipher 4 解密库
└── README.md
```

## 数据管线

```
第一步: 解密                      第二步: 蒸馏                    第三步: 模拟

微信 4.x 加密数据库          →   通过 LLM 提取人格           →   蒙特卡洛 N 次模拟

 ┌─ message_0.db ─┐                ┌─ persona A ─┐                ┌─ 时间线 1 ──┐
 │  contact.db     │         →     │  persona B   │         →     │  时间线 2    │
 │  session.db     │               └──────────────┘               │  ...         │
 └─────────────────┘                                              │  时间线 N    │
                                                                  └──────────────┘
                                                                        ↓
                                                                  P(X) = count(X) / N
```

## 第三方依赖

见 [third_party/README.md](third_party/README.md)
