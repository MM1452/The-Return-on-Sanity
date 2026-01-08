import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
INITIAL_WEALTH = 100_000
YEARS = 30
AVG_RETURN = 0.07 

# --- SCENARIO A: The Linear Model ---
linear_path = [INITIAL_WEALTH]
for _ in range(YEARS):
    linear_path.append(linear_path[-1] * (1 + AVG_RETURN))

# --- SCENARIO B: The Early Shock ---
reality_path = [INITIAL_WEALTH]
# Year 1 is -15%, next 2 years flat, then 7% growth
returns = [-0.15, 0.0, 0.0] + [AVG_RETURN] * (YEARS - 3)

for r in returns:
    reality_path.append(reality_path[-1] * (1 + r))

# --- PLOT ---
plt.figure(figsize=(10, 6))
plt.style.use('dark_background')
plt.plot(linear_path, label='The Model (Linear 7%)', linestyle='--', color='cyan')
plt.plot(reality_path, label='The Reality (Early Shock)', color='red', linewidth=3)
plt.title('Part I: The Cost of Sequence Risk')
plt.legend()
plt.show()