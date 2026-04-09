# Simulator / 蒙特卡洛模拟器

Given distilled personas, simulate N timelines and compute outcome probabilities.

给定蒸馏后的 persona，模拟 N 条时间线，计算结果概率分布。

```
persona A + persona B
        ↓
   N parallel simulations (Monte Carlo)
        ↓
   P(outcome) = count(outcome) / N
```

Each simulation branches at decision points — different choices, different timing, different moods — producing a distribution of possible futures from the same starting conditions.

每次模拟在决策点分叉 — 不同的选择、不同的时机、不同的心情 — 从相同初始条件产生一组可能的未来分布。
