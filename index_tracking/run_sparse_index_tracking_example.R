# run_sparse_index_tracking_example.R

# Load necessary libraries
library(sparseIndexTracking)
library(xts)

# Load the example data
data(INDEX_2010)

# Prepare training and testing data
X_train <- INDEX_2010$X[1:126]
X_test <- INDEX_2010$X[127:252]
r_train <- INDEX_2010$SP500[1:126]
r_test <- INDEX_2010$SP500[127:252]

# Design portfolios using different tracking measures

# ETE
w_ete <- spIndexTrack(X_train, r_train, lambda = 1e-7, u = 0.5, measure = 'ete')
cat('Number of assets used in ETE:', sum(w_ete > 1e-6), '\n')

# DR
w_dr <- spIndexTrack(X_train, r_train, lambda = 2e-8, u = 0.5, measure = 'dr')
cat('Number of assets used in DR:', sum(w_dr > 1e-6), '\n')

# HETE
w_hete <- spIndexTrack(X_train, r_train, lambda = 8e-8, u = 0.5, measure = 'hete', hub = 0.05)
cat('Number of assets used in HETE:', sum(w_hete > 1e-6), '\n')

# HDR
w_hdr <- spIndexTrack(X_train, r_train, lambda = 2e-8, u = 0.5, measure = 'hdr', hub = 0.05)
cat('Number of assets used in HDR:', sum(w_hdr > 1e-6), '\n')

# Evaluate portfolios by plotting cumulative P&L
plot(cbind("PortfolioETE" = cumprod(1 + X_test %*% w_ete), "S&P500" = cumprod(1 + r_test)), 
     legend.loc = "topleft", main = "Cumulative P&L - ETE")

plot(cbind("PortfolioDR" = cumprod(1 + X_test %*% w_dr), "S&P500" = cumprod(1 + r_test)),
     legend.loc = "topleft", main = "Cumulative P&L - DR")

plot(cbind("PortfolioHETE" = cumprod(1 + X_test %*% w_hete), "S&P500" = cumprod(1 + r_test)),
     legend.loc = "topleft", main = "Cumulative P&L - HETE")

plot(cbind("PortfolioHDR" = cumprod(1 + X_test %*% w_hdr), "S&P500" = cumprod(1 + r_test)),
     legend.loc = "topleft", main = "Cumulative P&L - HDR")