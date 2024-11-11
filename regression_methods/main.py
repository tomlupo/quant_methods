import numpy as np
import pandas as pd
from scipy.optimize import minimize

# Generate example data for asset returns and index returns
np.random.seed(42)
dates = pd.date_range(start='2020-01-01', periods=100, freq='B')
assets = pd.DataFrame(np.random.normal(0, 0.01, (100, 4)), columns=['Asset1', 'Asset2', 'Asset3', 'Asset4'], index=dates)
index_returns = pd.Series(np.random.normal(0, 0.01, 100), index=dates, name='Index')

def optimize_weights(method="ols", alpha=0.1, l1_ratio=0.5):
    """
    Optimize asset weights to replicate an index using different regression methods.

    This function uses `scipy.optimize.minimize` to find the optimal weights for
    replicating a target index with a portfolio of assets. Different regression
    methods can be used, each with unique regularization characteristics:
    - OLS: Ordinary Least Squares, with no regularization.
    - Ridge: L2 regularization to shrink weights, reducing potential overfitting.
    - Lasso: L1 regularization to promote sparsity, setting some weights to zero.
    - Elastic Net: Combination of L1 and L2 regularization, controlled by `l1_ratio`.

    Parameters
    ----------
    method : str, optional
        The regression method to use. Options are "ols" (default), "ridge", "lasso", and "elastic_net".
    alpha : float, optional
        The regularization strength, used for "ridge", "lasso", and "elastic_net". Default is 0.1.
    l1_ratio : float, optional
        The mix ratio of L1 to L2 penalty for "elastic_net". Ignored for other methods. Default is 0.5.
        - l1_ratio=1 corresponds to Lasso.
        - l1_ratio=0 corresponds to Ridge.

    Returns
    -------
    pd.Series
        A pandas Series with the optimized weights for each asset.

    Raises
    ------
    ValueError
        If an invalid method is passed.

    Notes
    -----
    - The weights are constrained to sum to 1.
    - Bounds are set between 0 and 1 to prevent short-selling.

    Examples
    --------
    >>> optimize_weights(method="ridge", alpha=0.1)
    """
    
    # Define the objective function based on the chosen method
    def objective(weights):
        # Calculate portfolio returns based on current weights
        portfolio_returns = assets.dot(weights)
        tracking_error = np.sum((portfolio_returns - index_returns) ** 2)
        
        # Add regularization penalty if applicable
        if method == "ols":
            # OLS: No regularization, just minimize tracking error
            return tracking_error
        elif method == "ridge":
            # Ridge: L2 penalty (sum of squares of weights)
            penalty = alpha * np.sum(weights ** 2)
            return tracking_error + penalty
        elif method == "lasso":
            # Lasso: L1 penalty (sum of absolute values of weights)
            penalty = alpha * np.sum(np.abs(weights))
            return tracking_error + penalty
        elif method == "elastic_net":
            # Elastic Net: Combination of L1 and L2 penalties
            l1_penalty = l1_ratio * alpha * np.sum(np.abs(weights))
            l2_penalty = (1 - l1_ratio) * alpha * np.sum(weights ** 2)
            return tracking_error + l1_penalty + l2_penalty
        else:
            raise ValueError("Invalid method. Choose from 'ols', 'ridge', 'lasso', 'elastic_net'.")

    # Initial weights (start with equal distribution)
    initial_weights = np.ones(assets.shape[1]) / assets.shape[1]
    
    # Constraints: Weights must sum to 1
    constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
    
    # Bounds: Set bounds to (0, 1) if we don't allow short-selling
    bounds = [(0, 1) for _ in range(assets.shape[1])]
    
    # Run optimization
    result = minimize(objective, initial_weights, constraints=constraints, bounds=bounds)
    
    # Retrieve optimized weights and put into a pandas Series
    optimized_weights = pd.Series(result.x, index=assets.columns, name=f"{method.capitalize()} Weight")
    
    return optimized_weights

# Example usage:
# OLS
ols_weights = optimize_weights(method="ols")
print("\nOLS Weights:")
print(ols_weights)
print("Sum of OLS Weights:", ols_weights.sum())

# Ridge
ridge_weights = optimize_weights(method="ridge", alpha=0.1)
print("\nRidge Weights:")
print(ridge_weights)
print("Sum of Ridge Weights:", ridge_weights.sum())

# Lasso
lasso_weights = optimize_weights(method="lasso", alpha=0.1)
print("\nLasso Weights:")
print(lasso_weights)
print("Sum of Lasso Weights:", lasso_weights.sum())

# Elastic Net
elastic_net_weights = optimize_weights(method="elastic_net", alpha=0.1, l1_ratio=0.5)
print("\nElastic Net Weights:")
print(elastic_net_weights)
print("Sum of Elastic Net Weights:", elastic_net_weights.sum())
