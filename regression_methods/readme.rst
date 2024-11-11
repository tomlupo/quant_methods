Code Explanation
================

Data Generation
---------------
The example uses randomly generated asset and index returns data. Replace this with real data for practical use.

Function `optimize_weights`
---------------------------

Parameters
~~~~~~~~~~
- **method**: Specifies the regression type (OLS, Ridge, Lasso, or Elastic Net).
- **alpha**: Regularization strength, relevant for Ridge, Lasso, and Elastic Net.
- **l1_ratio**: Balance between L1 and L2 penalties for Elastic Net, where ``l1_ratio=1`` means full Lasso and ``l1_ratio=0`` is full Ridge.

Objective Function
------------------
- **Tracking Error**: Calculated as the squared difference between portfolio and index returns.

- **Regularization**:
  - **OLS**: No regularization, minimizing tracking error alone.
  - **Ridge**: Adds an L2 penalty proportional to ``alpha * sum(weights ** 2)``.
  - **Lasso**: Adds an L1 penalty proportional to ``alpha * sum(abs(weights))``.
  - **Elastic Net**: Combines L1 and L2 penalties, controlled by `l1_ratio` and `alpha`.

Optimization Setup
------------------
- **Initial Weights**: Starts with equal weights for simplicity.
- **Constraints**: Enforces that weights sum to 1.
- **Bounds**: Keeps weights between 0 and 1, preventing short-selling.

Results
-------
- The function returns optimized weights as a pandas Series.
- Example usage demonstrates weight optimization for each method, displaying results and checking that the sum of weights is 1.

This setup provides a flexible, modular approach to regression-based index replication, with options for OLS, Ridge, Lasso, and Elastic Net, and clear parameterization for different regularization strengths.
