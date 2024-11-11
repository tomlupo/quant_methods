# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 10:05:10 2024

@author: twilc
"""

import numpy as np
import matplotlib.pyplot as plt

# Set random seed for reproducibility
np.random.seed(42)

# Simulation parameters
S0 = 100  # Initial stock price
T = 1  # Time horizon (1 year)
N = 252  # Number of time steps (trading days)
dt = T / N  # Time step size
num_simulations = 1000  # Number of Monte Carlo simulations

# Estimated parameters
estimated_mu = 0.10  # Estimated annual return (10%)
sigma = 0.20  # Annual volatility (20%)

# Incorporate parameter uncertainty
mu_error = 0.02  # 2% error in mean estimate
mu_lower = estimated_mu - mu_error
mu_upper = estimated_mu + mu_error

def simulate_gbm(S0, mu, sigma, T, N):
    """Simulate a single path of Geometric Brownian Motion."""
    t = np.linspace(0, T, N)
    W = np.random.standard_normal(size=N)
    W = np.cumsum(W) * np.sqrt(dt)  # Cumulative sum for Brownian motion
    X = (mu - 0.5 * sigma**2) * t + sigma * W
    S = S0 * np.exp(X)
    return S

def run_simulation(num_simulations, with_error=False):
    simulation_results = []
    for _ in range(num_simulations):
        if with_error:
            # Sample mu from uniform distribution to incorporate uncertainty
            mu = np.random.uniform(mu_lower, mu_upper)
        else:
            mu = estimated_mu
        
        # Simulate a single path
        S = simulate_gbm(S0, mu, sigma, T, N)
        simulation_results.append(S)
    
    return np.array(simulation_results)

# Run simulations
results_without_error = run_simulation(num_simulations, with_error=False)
results_with_error = run_simulation(num_simulations, with_error=True)

# Calculate statistics
def calculate_stats(results):
    mean_path = np.mean(results, axis=0)
    lower_bound = np.percentile(results, 5, axis=0)
    upper_bound = np.percentile(results, 95, axis=0)
    final_prices = results[:, -1]
    return mean_path, lower_bound, upper_bound, final_prices

stats_without_error = calculate_stats(results_without_error)
stats_with_error = calculate_stats(results_with_error)

# Plotting
plt.figure(figsize=(12, 6))

# Plot without error
plt.subplot(1, 2, 1)
plt.plot(stats_without_error[0], label='Mean Path')
plt.fill_between(range(N), stats_without_error[1], stats_without_error[2], alpha=0.3, label='90% CI')
plt.plot(results_without_error[:10].T, alpha=0.1, color='gray')
plt.title('Without Parameter Error')
plt.xlabel('Trading Days')
plt.ylabel('Stock Price')
plt.legend()
plt.grid(True)

# Plot with error
plt.subplot(1, 2, 2)
plt.plot(stats_with_error[0], label='Mean Path')
plt.fill_between(range(N), stats_with_error[1], stats_with_error[2], alpha=0.3, label='90% CI')
plt.plot(results_with_error[:10].T, alpha=0.1, color='gray')
plt.title('With Parameter Error')
plt.xlabel('Trading Days')
plt.ylabel('Stock Price')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# Print statistics
def print_stats(name, stats):
    print(f"\n{name}:")
    print(f"Expected final price: ${stats[0][-1]:.2f}")
    print(f"90% CI for final price: (${stats[1][-1]:.2f}, ${stats[2][-1]:.2f})")
    print(f"Probability of price increase: {np.mean(stats[3] > S0):.2%}")
    print(f"Standard deviation of final price: ${np.std(stats[3]):.2f}")

print_stats("Without Parameter Error", stats_without_error)
print_stats("With Parameter Error", stats_with_error)