# Distillation Is All You Need

> 蒸馏即一切 —— 把真实的人蒸馏成数据，模拟命运，计算可能性。

## Quick Start

```bash
# 1. 克隆
git clone https://github.com/dotafs/Distillation-Is-All-You-Need.git
cd Distillation-Is-All-You-Need

# 2. 环境搭建（下载工具 + 安装依赖）
python pipeline/setup.py

# 3. 解密微信数据库（需管理员终端 + 微信 4.x 已登录运行）
python pipeline/decrypt_wx4.py
```

解密后的数据库在 `third_party/wechat-decrypt/decrypted/`，可直接用 SQLite 浏览。

## 项目结构

```
Distillation-Is-All-You-Need/
├── simulator/              # AI 缘分模拟器
├── pipeline/               # 数据处理 pipeline
│   ├── setup.py            # 一键环境搭建
│   └── decrypt_wx4.py      # 微信 4.x 数据库解密
├── third_party/            # 第三方依赖（见 third_party/README.md）
│   ├── WeChatMsg/          # 微信聊天记录导出工具 (3.x)
│   └── wechat-decrypt/     # 微信 4.x 数据库解密库
└── README.md
```

## 核心思路

\\\
真实聊天记录 / 日记 / 原始文档
        ↓
    persona 蒸馏（Claude API）
        ↓
    Monte Carlo 时间线模拟（N 条）
        ↓
    在一起的概率 + 每条时间线剧情
\\\

## Third Party

详见 [third_party/README.md](third_party/README.md)
