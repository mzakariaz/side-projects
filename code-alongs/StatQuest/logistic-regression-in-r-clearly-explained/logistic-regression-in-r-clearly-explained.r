# Load packages
library(ggplot2)
library(cowplot)
library(rstudioapi)

# Get the file path of the current script:
current_directory_name <- dirname(getSourceEditorContext()$path)

# Load the dataset
url <- "https://raw.githubusercontent.com/StatQuest/logistic_regression_demo/master/processed.cleveland.data"
data <- read.csv(url, header = FALSE)

# Display the first few rows of the dataset
head(data)

# Add headers to the dataset
colnames(data) <- c(
  "age",
  "sex",
  "cp",
  "trestbps",
  "chol",
  "fbs",
  "restecg",
  "thalach",
  "exang",
  "oldpeak",
  "slope",
  "ca",
  "thal",
  "hd"
)

# Inspect the structure of the dataset
str(data)

# Clean the dataset
data[data == "?"] <- NA
data[data$sex == 0, ]$sex <- "F"
data[data$sex == 1, ]$sex <- "M"
data$sex <- as.factor(data$sex)
data$cp <- as.factor(data$cp)
data$fbs <- as.factor(data$fbs)
data$restecg <- as.factor(data$restecg)
data$exang <- as.factor(data$exang)
data$slope <- as.factor(data$slope)
data$ca <- as.integer(data$ca)
data$ca <- as.factor(data$ca)
data$thal <- as.integer(data$thal)
data$thal <- as.factor(data$thal)
data$hd <- ifelse(test = data$hd == 0, yes = "Healthy", no = "Unhealthy")
data$hd <- as.factor(data$hd)

# Inspect the structure of the dataset again
str(data)

# Print the number of rows of data with NA values
print(nrow(data[is.na(data$ca) | is.na(data$thal), ]))

# Select the rows of data with NA values
print(data[is.na(data$ca) | is.na(data$thal), ])

# Count the number of rows in the dataset
print(nrow(data))

# Remove the rows of data with NA values
data <- data[!(is.na(data$ca) | is.na(data$thal)), ]

# Count the number of rows in the dataset again
print(nrow(data))

# Build a contingency table using heart disease and sex from the dataset
print(xtabs(~ hd + sex, data = data))

# Build a contingency table using heart disease and fbs from the dataset
print(xtabs(~ hd + fbs, data = data))

# Build a contingency table using heart disease and restecg from the dataset
print(xtabs(~ hd + restecg, data = data))

# Build a contingency table using heart disease and exang from the dataset
print(xtabs(~ hd + exang, data = data))

# Build a contingency table using heart disease and slope from the dataset
print(xtabs(~ hd + slope, data = data))

# Build a contingency table using heart disease and ca from the dataset
print(xtabs(~ hd + ca, data = data))

# Build a contingency table using heart disease and thal from the dataset
print(xtabs(~ hd + thal, data = data))

# Define a logistic regression to the dataset predicting hd from sex
logistic <- glm(hd ~ sex, data = data, family = "binomial")

# Print the summary of this logistic regression model
print(summary(logistic))

# Define a logistic regression to the dataset predicting hd generally
logistic <- glm(hd ~ ., data = data, family = "binomial")

# Print the summary of this logistic regression model
print(summary(logistic))

# Calculate the McFadden's Pseudo R^2 and p-value for the logistic regression
ll_null <- logistic$null.deviance / -2
ll_proposed <- logistic$deviance / -2
mcfadden_pseudo_r_squared <- (ll_null - ll_proposed) / ll_null
print(mcfadden_pseudo_r_squared)
p_value <- 1 - pchisq(
  2 * (ll_proposed - ll_null),
  df = length(logistic$coefficients) - 1
)
print(p_value)

# Draw the logistic regression curve
predicted_data <- data.frame(
  probability.of.hd = logistic$fitted.values,
  hd = data$hd
)
predicted_data <- predicted_data[
  order(predicted_data$probability.of.hd, decreasing = FALSE),
]

n <- nrow(predicted_data)
predicted_data$rank <- 1:n

logistic_regression_plot <- ggplot(
  data = predicted_data,
  aes(x = rank, y = probability.of.hd)
) +
  geom_point(aes(color = hd), alpha = 1, shape = 4, stroke = 2) +
  xlab("Index") +
  ylab("Predicted probability of getting heart disease")

print(logistic_regression_plot)

# Save the plot as a .png image
file_name <- "/heart_disease_probabilities.png"
file_path <- paste(
  current_directory_name,
  file_name,
  sep = ""
)

ggsave(filename = file_path)