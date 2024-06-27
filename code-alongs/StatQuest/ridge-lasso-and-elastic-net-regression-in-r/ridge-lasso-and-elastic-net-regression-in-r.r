# CREDIT:
# Ridge, Lasso and Elastic-Net Regression in R
# (published on Tuesday 23 October 2018)
# URL: https://www.youtube.com/watch?v=ctmNq7FgbvI

# Load packages
library(ggplot2)
library(cowplot)
library(rstudioapi)
library(glmnet)

# Get the file path of the current script:
current_directory_name <- dirname(getSourceEditorContext()$path)

# Set a random seed value
set.seed(42)

# Define the desired dimensions of a randomly generated dataset
n <- 1000                   # Number of rows
total_parameters <- 5000    # Number of columns
important_parameters <- 15  # Number of important columns

# Define the predictor variables (feature matrix) of the dataset
x <- matrix(
  rnorm(n * total_parameters, mean = 0, sd = 1),
  nrow = n,
  ncol = total_parameters
)

# Define the target variable (or target vector) for the dataset
y <- apply(
  x[, 1:important_parameters],
  1,
  sum
) +
  rnorm(n, mean = 0, sd = 1)

# Randomly choose the training set's row indices in the dataset
train_rows <- sample(1:n, .66 * n)

# Split the dataset into a training set and a testing set
x_train <- x[train_rows, ] # Training set predictor variables
x_test <- x[-train_rows, ] # Testing set predictor variables
y_train <- y[train_rows] # Training set target variable
y_test <- y[-train_rows] # Testing set target variable

# Fit a Ridge regression model to the training data
# using 10-fold cross-validation to obtain optimal
# values for the lambda hyperparameter
ridge_regression <- cv.glmnet(
  x_train,
  y_train,
  type.measure = "mse",
  alpha = 0,
  family = "gaussian"
)

# Predict the values of the target variable on the
# testing set using the fitted Ridge Regression model
y_pred_ridge_regression <- predict(
  ridge_regression,
  s = ridge_regression$lambda.min,
  newx = x_test
)

# Calculate and display the Mean Squared Error of the
# fitted Ridge Regression model on the testing set
mse_ridge_regression <- mean((y_pred_ridge_regression - y_test)^2)
print(
  paste(
    "Ridge Regression Mean Squared Error:",
    as.character(mse_ridge_regression),
    sep = " "
  )
)

# Fit a Lasso regression model to the training data
# using 10-fold cross-validation to obtain optimal
# values for the lambda hyperparameter
lasso_regression <- cv.glmnet(
  x_train,
  y_train,
  type.measure = "mse",
  alpha = 1,
  family = "gaussian"
)

# Predict the values of the target variable on the
# testing set using the fitted Lasso Regression model
y_pred_lasso_regression <- predict(
  lasso_regression,
  s = lasso_regression$lambda.min,
  newx = x_test
)

# Calculate and display the Mean Squared Error of the
# fitted Lasso Regression model on the testing set
mse_lasso_regression <- mean((y_pred_lasso_regression - y_test)^2)
print(
  paste(
    "Lasso Regression Mean Squared Error:",
    as.character(mse_lasso_regression),
    sep = " "
  )
)

# Fit an Elastic-Net regression model to the training data
# using 10-fold cross-validation to obtain optimal
# values for the lambda hyperparameter
elastic_net_regression <- cv.glmnet(
  x_train,
  y_train,
  type.measure = "mse",
  alpha = 0.5,
  family = "gaussian"
)

# Predict the values of the target variable on the
# testing set using the fitted Elastic-Net Regression model
y_pred_elastic_net_regression <- predict(
  elastic_net_regression,
  s = elastic_net_regression$lambda.min,
  newx = x_test
)

# Calculate and display the Mean Squared Error of the
# fitted Elastic-Net Regression model on the testing set
mse_elastic_net_regression <- mean((y_pred_elastic_net_regression - y_test)^2)
print(
  paste(
    "Elastic-Net Regression Mean Squared Error:",
    as.character(mse_elastic_net_regression),
    sep = " "
  )
)

# Fit one-hundred Elastic-Net regression models to the training data
# using 10-fold cross-validation to obtain optimal values for the
# lambda hyperparameter
list_of_fits <- list()
for (i in 0:10) {
  fit_name <- paste("alpha_", i / 10, sep = "")
  list_of_fits[[fit_name]] <-
    cv.glmnet(
      x_train,
      y_train,
      type.measure = "mse",
      alpha = i / 10,
      family = "gaussian"
    )
}

# Create an empty dataframe
results <- data.frame()

# For each of the one-hundred fits, retrieve the value of alpha,
# the fit name, and the mean squared error, store them as a row
# and bind it to the dataframe
for (i in 0:10) {
  fit_name <- paste("alpha_", i / 10, sep = "")
  y_pred_fit <- predict(
    list_of_fits[[fit_name]],
    s = list_of_fits[[fit_name]]$lambda.min,
    newx = x_test
  )
  mse_fit <- mean((y_pred_fit - y_test)^2)
  temp <- data.frame(alpha = i / 10, mse_fit = mse_fit, fit_name = fit_name)
  results <- rbind(results, temp)
}

# Print the resulting dataframe
print(results)

# Plot the mean squared error of the fit against the value of alpha
results_plot <- ggplot(
  data = results,
  aes(x = alpha, y = mse_fit)
) +
  geom_point(alpha = 1, shape = 4, stroke = 2) +
  xlab("Alpha") +
  ylab("Mean Squared Error") +
  ggtitle("Mean Squared Errors for Elastic-Net Regression")
print(results_plot)

# Save the plot as a .png image
file_name <- "/mean-squared-errors-for-elastic-net-regression.png"
file_path <- paste(
  current_directory_name,
  file_name,
  sep = ""
)
ggsave(filename = file_path)