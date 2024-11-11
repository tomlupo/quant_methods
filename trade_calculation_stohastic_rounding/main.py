import pandas as pd
import math
import random

def stochastic_round_lot(value, lot_size):
    lower_multiple = math.floor(value / lot_size) * lot_size
    upper_multiple = math.ceil(value / lot_size) * lot_size
    decimal_part = (value - lower_multiple) / lot_size
    rand = random.random()
    if rand <= decimal_part:
        return upper_multiple
    else:
        return lower_multiple

def calculate_trades(target_weights, current_positions, prices, lot_size):
    total_value = sum(current_positions[asset] * prices[asset] for asset in current_positions)
    desired_positions = {}
    final_details = []

    for asset in current_positions:
        current_value = current_positions[asset] * prices[asset]
        current_weight = (current_value / total_value) * 100

        target_weight = target_weights.get(asset, 0)  # Default to 0 if no target weight specified
        target_value = (target_weight / 100) * total_value
        unrounded_shares = target_value / prices[asset]
        rounded_shares = stochastic_round_lot(unrounded_shares, lot_size.get(asset, 1))  # Default lot size 1 if not specified
        trade_size = rounded_shares - current_positions.get(asset, 0)
        final_position = current_positions.get(asset, 0) + trade_size
        final_value = final_position * prices[asset]
        final_weight = (final_value / total_value) * 100

        final_details.append({
            'Asset': asset,
            'Current Position': current_positions[asset],
            'Price': prices[asset],
            'Current Weight (%)': current_weight,
            'Target Weight (%)': target_weight,
            'Lot Size': lot_size[asset],
            'Trade (Shares)': trade_size,
            'Final Position (Shares)': final_position,
            'Final Weight (%)': final_weight
        })

    return pd.DataFrame(final_details)

# Example usage
target_weights = {'StockA': 30, 'StockB': 50, 'StockC': 20}
current_positions = {'StockA': 100, 'StockB': 200, 'StockC': 50}
prices = {'StockA': 50, 'StockB': 25, 'StockC': 100}
lot_sizes = {'StockA': 10, 'StockB': 5, 'StockC': 1}

df_trades = calculate_trades(target_weights, current_positions, prices, lot_sizes)
print(df_trades)
