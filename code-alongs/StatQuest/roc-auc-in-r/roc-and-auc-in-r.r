# CREDIT:
# StatQuest - ROC and AUC in R (published on Tuesday 18 December 2018)
# URL: https://www.youtube.com/watch?v=qcvAqAH60Yw

# Install packages
library(pROC)
library(randomForest)
library(rstudioapi)

# Get the file path of the current script:
current_directory_name <- dirname(getSourceEditorContext()$path)

# Set random seed value
set.seed(42)

# Initialise parameters
num_samples <- 100
mean <- 172
sd <- 29
min <- 0
max <- 1

# Build the obese classification
weight <- sort(rnorm(n = num_samples, mean = mean, sd = sd))
random <- runif(n = num_samples, min = 0, max = 1)
obese <- ifelse(test = (random < rank(weight) / num_samples), yes = 1, no = 0)

# Print the obese classification
print(obese)

# Set the working directory to the current directory
setwd(normalizePath(getwd()))


# Use as much space as possible for the plots
par(pty = "m")

# Plot the obese classification by weight
plot(x = weight, y = obese)

# Fit a logistic regression to the weights and obese classification
glm_fit <- glm(obese ~ weight, family = binomial)

# Predict the probabilities associated to the logistic regression
predicted_probs <- predict(glm_fit, type = "response")

# Draw the logistic regression curve associated to the predicted probabilities
lines(weight, predicted_probs)

# Save the plot as a .png image
file_name_1 <- "/logistic_regression.png"
file_path_1 <- paste(
  current_directory_name,
  file_name_1,
  sep = ""
)
dev.copy(png, file = file_path_1)
dev.off()

# Initialise a random forest model
rf_model <- randomForest(factor(obese) ~ weight)

# Use as much space as possible for the plot
par(pty = "m")

# Build and plot the ROC for the logistic regression
roc_info <- roc(
  obese,
  predicted_probs,
  plot = TRUE,
  legacy.axes = TRUE,
  percent = TRUE,
  xlab = "False Positive Percentage (1 - Specificity)",
  ylab = "True Positive Percentage (Sensitivity)",
  col = "#377eb8",
  lwd = 4,
  print.auc = TRUE,
  print.auc.x = 45,
  partial.auc = c(100, 90),
  auc.polygon = TRUE,
  auc.polygon.col = "#377eb822"
)

# Build and plot the ROC for the random forest model
plot.roc(
  obese,
  rf_model$votes[, 1],
  percent = TRUE,
  col = "#4daf4a",
  lwd = 4,
  print.auc = TRUE,
  add = TRUE,
  print.auc.y = 40,
  partial.auc = c(100, 90),
  auc.polygon = TRUE,
  auc.polygon.col = "#4daf4a22"
)

# Add a legend to the plot
legend(
  "bottomright",
  legend = c("Logistic Regression", "Random Forest"),
  col = c("#377eb8", "#4daf4a"),
  lwd = 4
)

# Save the plot as a .png image
file_name_2 <- "/roc-auc-logistic-regression-random-forest.png"
file_path_2 <- paste(
  current_directory_name,
  file_name_2,
  sep = ""
)
dev.copy(png, file = file_path_2)
dev.off()

# Tabulate the sensitivities and specificities of the logistic regression's ROC
roc_df <- data.frame(
  tpp = roc_info$sensitivities,
  fpp = (100 - roc_info$specificities),
  thresholds = roc_info$thresholds
)

# Print the head, the tail and a subset of the tabulated ROC data
print("Head:")
print(head(roc_df))

print("Tail:")
print(tail(roc_df))

print("Subset:")
print(roc_df[roc_df$tpp > 60 & roc_df$tpp < 80, ])