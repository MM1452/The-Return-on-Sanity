import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
initial_wealth = 100
num_people = 2000      # The "Ensemble" size
num_time_steps = 100   # Duration
win_pct = 0.50         # Gain 50%
loss_pct = 0.40        # Lose 40%
leverage = 1.0         # 1.0 = Betting 100% of equity (The "Part 2" Trap)

# --- SIMULATION ---
# Initialize wealth array (Rows = People, Cols = Time)
wealth_paths = np.zeros((num_people, num_time_steps))
wealth_paths[:, 0] = initial_wealth

np.random.seed(42) # Fixed seed ensures your article stats stay consistent

for t in range(1, num_time_steps):
    # Flip coin: 1 = Head, 0 = Tail
    coin_flips = np.random.choice([0, 1], size=num_people, p=[0.5, 0.5])
    
    # Calculate returns based on leverage
    # If leverage is 1.0, we gain 50% or lose 40% of TOTAL equity
    current_step_return = np.where(coin_flips == 1, win_pct, -loss_pct)
    
    # Apply return to previous wealth
    wealth_paths[:, t] = wealth_paths[:, t-1] * (1 + leverage * current_step_return)

# --- STATISTICS FOR ARTICLE TEXT ---
ensemble_average = np.mean(wealth_paths, axis=0)
median_path = np.median(wealth_paths, axis=0)

# Calculate Survivors vs Ruin
final_wealth = wealth_paths[:, -1]
winners = np.sum(final_wealth > initial_wealth)
losers = num_people - winners
win_rate = (winners / num_people) * 100
loss_rate = (losers / num_people) * 100

print(f"--- ARTICLE STATISTICS ---")
print(f"Average Wealth (The Model): ${ensemble_average[-1]:,.0f}")
print(f"Median Wealth (The Reality): ${median_path[-1]:,.2f}")
print(f"Total Participants: {num_people}")
print(f"Participants who lost money: {losers} ({loss_rate:.1f}%)")

# --- VISUALIZATION (THE SPAGHETTI CHART) ---
plt.figure(figsize=(12, 7))
plt.style.use('dark_background')

# 1. The "White Cloud" (Individual Paths)
# Alpha is set very low (0.03) to create the 'heatmap' effect of the swarm
plt.plot(wealth_paths.T, color='white', alpha=0.03, linewidth=1)

# 2. The "Blue Line" (Ensemble Average)
plt.plot(ensemble_average, color='#00d1ff', linewidth=4, label='Ensemble Average (The Model)')

# 3. The "Red Line" (Median/Reality)
plt.plot(median_path, color='#ff4d4d', linewidth=4, linestyle='--', label='Median Path (The Reality)')

# Formatting
plt.title(f'The Thermostat of Ruin: Volatility Drag in Action\n(Bet Size: {leverage*100:.0f}% of Equity)', fontsize=14, pad=20)
plt.ylabel('Wealth ($) - Log Scale', fontsize=12)
plt.xlabel('Time (Bets)', fontsize=12)
plt.yscale('log') # CRITICAL: Log scale shows the true divergence
plt.grid(color='grey', linestyle=':', alpha=0.3)
plt.legend(loc='upper left', fontsize=11)
plt.axhline(y=initial_wealth, color='yellow', linestyle=':', alpha=0.5, linewidth=1) # Breakeven

# Annotation for impact
plt.annotate('The Ergodicity Gap', 
             xy=(num_time_steps-1, ensemble_average[-1]), 
             xytext=(num_time_steps-40, median_path[-1]*1000),
             arrowprops=dict(facecolor='white', shrink=0.05),
             fontsize=12, color='white', weight='bold')

plt.tight_layout()
plt.show()