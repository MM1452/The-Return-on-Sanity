import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# --- CONFIGURATION ---
INITIAL_WEALTH = 100
NUM_PEOPLE = 2000       # The "Ensemble" size
NUM_TIME_STEPS = 100    # Duration (Number of bets)
WIN_PCT = 0.50          # Gain 50%
LOSS_PCT = 0.40         # Lose 40%
LEVERAGE = 1.0          # 1.0 = Betting 100% of equity (The "Part 2" Trap)

# --- SIMULATION ---
np.random.seed(42)  # Fixed seed for reproducibility in article

# Initialize wealth array (Rows = People, Cols = Time)
wealth_paths = np.zeros((NUM_PEOPLE, NUM_TIME_STEPS))
wealth_paths[:, 0] = INITIAL_WEALTH

for t in range(1, NUM_TIME_STEPS):
    # Flip coin: 1 = Head (Win), 0 = Tail (Loss)
    # shape=(NUM_PEOPLE,) creates a unique flip for every person
    coin_flips = np.random.choice([0, 1], size=NUM_PEOPLE, p=[0.5, 0.5])
    
    # Calculate returns based on leverage
    # If head: +50% * leverage. If tail: -40% * leverage.
    current_step_return = np.where(coin_flips == 1, WIN_PCT, -LOSS_PCT)
    
    # Apply return to previous wealth
    wealth_paths[:, t] = wealth_paths[:, t-1] * (1 + LEVERAGE * current_step_return)

# --- STATISTICS ---
ensemble_average = np.mean(wealth_paths, axis=0)
median_path = np.median(wealth_paths, axis=0)

# Calculate Survivors vs Ruin
final_wealth = wealth_paths[:, -1]
winners = np.sum(final_wealth > INITIAL_WEALTH)
losers = NUM_PEOPLE - winners
loss_rate = (losers / NUM_PEOPLE) * 100

print(f"--- ARTICLE STATISTICS ---")
print(f"Ensemble Average (Theoretical Expectation): ${ensemble_average[-1]:,.0f}")
print(f"Median Wealth (Typical Experience):         ${median_path[-1]:,.2f}")
print(f"Break-even rate:                            {100 - loss_rate:.1f}%")
print(f"Ruin rate (Wealth < Initial):               {loss_rate:.1f}%")

# --- VISUALIZATION ---
plt.figure(figsize=(12, 7))
plt.style.use('dark_background')

# 1. The "Cloud" (Individual Paths)
# We plot a subset or use low alpha to prevent rendering lag if N is huge
plt.plot(wealth_paths.T, color='white', alpha=0.02, linewidth=1)

# 2. The "Blue Line" (Ensemble Average)
plt.plot(ensemble_average, color='#00d1ff', linewidth=3, label='Ensemble Average (Arithmetic Mean)')

# 3. The "Red Line" (Median/Reality)
plt.plot(median_path, color='#ff4d4d', linewidth=3, linestyle='--', label='Median Path (Geometric Mean)')

# Formatting
plt.title(f'The Ergodicity Gap: Ensemble vs Time Average\n(Bet Size: {LEVERAGE*100:.0f}% of Equity)', fontsize=16, pad=20)
plt.ylabel('Wealth ($) - Log Scale', fontsize=12)
plt.xlabel('Time (Number of Bets)', fontsize=12)
plt.yscale('log') 

# Custom Y-axis formatter to make log scale readable ($100, $1k, etc)
plt.gca().yaxis.set_major_formatter(mticker.StrMethodFormatter('${x:,.0f}'))
plt.grid(color='grey', linestyle=':', alpha=0.3)
plt.legend(loc='upper left', fontsize=12)

# Breakeven Line
plt.axhline(y=INITIAL_WEALTH, color='yellow', linestyle=':', alpha=0.5, linewidth=1, label='Break Even')

# Dynamic Annotation 
# (Positions the text relative to the gap between the two lines at the end)
bbox_props = dict(boxstyle="round,pad=0.3", fc="black", ec="white", lw=1)
plt.annotate('The Ergodicity Gap\n(Volatility Drag)', 
             xy=(NUM_TIME_STEPS-1, ensemble_average[-1]), 
             xytext=(NUM_TIME_STEPS/2, np.sqrt(ensemble_average[-1] * median_path[-1])), # Placed geometrically between them
             arrowprops=dict(facecolor='white', arrowstyle='->', connectionstyle="arc3,rad=-0.2"),
             fontsize=12, color='white', weight='bold', ha='center', bbox=bbox_props)

plt.tight_layout()

# Save locally so you can upload the image to the article
plt.savefig('ergodicity_gap_chart.png', dpi=300)
plt.show()