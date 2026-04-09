# Distillation Is All You Need

> 蒸馏即一切 —— 把真实的人蒸馏成数据，模拟命运，计算可能性。

## 项目结构

\\\
Distillation-Is-All-You-Need/
├── simulator/          # AI 缘分模拟器
├── pipeline/           # 数据导出 → 蒸馏 → 喂给模拟器
├── third_party/        # 第三方依赖（见 third_party/README.md）
│   └── WeChatMsg/      # 微信聊天记录导出工具
└── README.md
\\\

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
