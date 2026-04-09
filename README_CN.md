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

### Step 0: 克隆

```bash
git clone https://github.com/dotafs2/Distillation-Is-All-You-Need.git
cd Distillation-Is-All-You-Need
```

### Step 1: 环境搭建（普通终端）

```bash
python pipeline/setup.py
```

下载 wx_key（微信 4.x 密钥提取器）+ 安装 Python 依赖（pycryptodome, zstandard, uiautomation, pywin32 等）。

### Step 2: 解密数据库（管理员终端，只需跑一次）

```bash
python pipeline/decrypt_wx4.py
```

需要**管理员权限**（读取微信进程内存）。微信必须正在运行且已登录。自动检测 wxid，提取 16 个 per-DB 加密密钥，解密全部数据库。

`--wxid wxid_xxx` 指定账号。`--keys-only` 只提取密钥不解密。

### Step 3: 读取消息（普通终端）

```bash
python pipeline/read_wx_msg.py              # 最新 10 条消息
python pipeline/read_wx_msg.py --last 20    # 最新 20 条
python pipeline/read_wx_msg.py --watch      # 实时轮询（每 3 秒）
```

无需管理员 — 使用 Step 2 保存的密钥。

### Step 4: 发送消息（普通终端，微信窗口需可见）

```bash
python pipeline/send_wx_msg.py --to "联系人昵称" --msg "你好"
python pipeline/send_wx_msg.py --to "联系人昵称" --msg "第一行" --msg "第二行"
```

使用 Windows UI 自动化（非 hook，不封号）。运行时几秒钟内不要动鼠标键盘。

## 项目结构

```
Distillation-Is-All-You-Need/
├── pipeline/                # 数据管线
│   ├── setup.py             #   一键环境搭建
│   ├── decrypt_wx4.py       #   微信 4.x 数据库解密（管理员，跑一次）
│   ├── read_wx_msg.py       #   从加密数据库读取/轮询消息
│   └── send_wx_msg.py       #   通过 UI 自动化发送消息
├── simulator/               # 蒙特卡洛模拟器（开发中）
├── third_party/             # 第三方依赖
│   ├── WeChatMsg/           #   微信 3.x 导出工具
│   ├── wechat-decrypt/      #   微信 4.x SQLCipher 4 解密库
│   └── WeChatMassTool/      #   微信消息发送（UI 自动化）
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

## 环境要求

- **系统**: Windows 10/11
- **微信**: 4.x（已测试 4.1.7.30）
- **Python**: 3.12+
- **管理员权限**: 仅 Step 2（密钥提取）需要

## 第三方依赖

见 [third_party/README.md](third_party/README.md)
