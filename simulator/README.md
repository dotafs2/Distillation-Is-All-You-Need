[**中文**](README_CN.md) | English

# Simulator

Given distilled personas, simulate N timelines and compute outcome probabilities.

```
persona A + persona B
        ↓
   N parallel simulations (Monte Carlo)
        ↓
   P(outcome) = count(outcome) / N
```

Each simulation branches at decision points — different choices, different timing, different moods — producing a distribution of possible futures from the same starting conditions.
