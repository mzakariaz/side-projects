# CREDIT:
# StatQuest: MDS and PCoA in R (published on Monday 18 December 2018)
# URL: https://www.youtube.com/watch?v=pGAUHhLYp5Q

# Load packages
library(ggplot2)
library(cowplot)
library(rstudioapi)

# Get the file path of the current script
current_directory_name <- dirname(getSourceEditorContext()$path)

# Create a matrix for the dataset
data_matrix <- matrix(nrow = 100, ncol = 10)

# Name the columns of the matrix
colnames(data_matrix) <- c(
  paste("wt", 1:5, sep = ""),
  paste("ko", 1:5, sep = "")
)

# Name the rows of the matrix
rownames(data_matrix) <- paste("gene", 1:100, sep = "")

# Define the entries of the matrix
for (i in 1:100) {
  wt_values <- rpois(5, lambda = sample(x = 10:1000, size = 1))
  ko_values <- rpois(5, lambda = sample(x = 10:1000, size = 1))
  data_matrix[i, ] <- c(wt_values, ko_values)
}

# Print the head of the matrix
print(head(data_matrix))

# Perform Principal Component Analysis (PCA) on the matrix
pca <- prcomp(t(data_matrix), scale = TRUE, center = TRUE)

# Calculate the variance and variance
# percentages of the matrix's principal components
pca_var <- pca$sdev^2
pca_var_per <- round(pca_var / sum(pca_var) * 100, 1)

# Print the variance percentages of the matrix's principal components
print(pca_var_per)

# Create a dataframe containing the matrix's first two principal components
pca_data <- data.frame(
  Sample = rownames(pca$x),
  X = pca$x[, 1],
  Y = pca$x[, 2]
)

# Print the matrix's first two principal components
print(pca_data)

# Plot the matrix's first two principal components
pca_plot <- ggplot(
  data = pca_data,
  aes(x = X, y = Y, label = Sample)
) +
  geom_text() +
  xlab(paste("PC1 - ", pca_var_per[1], "%", sep = "")) +
  ylab(paste("PC2 - ", pca_var_per[2], "%", sep = "")) +
  theme_bw() +
  ggtitle("My PCA Graph")
print(pca_plot)

# Save the plot as a .png image
file_name_1 <- "/pca-plot-1.png"
file_path_1 <- paste(
  current_directory_name,
  file_name_1,
  sep = ""
)
dev.copy(png, file = file_path_1)
dev.off()


# Create a distance matrix from the data using Euclidean distance
distance_matrix <- dist(
  scale(t(data_matrix), center = TRUE, scale = TRUE),
  method = "euclidean"
)

# Apply multidimensional scaling to the distance matrix
mds_values <- cmdscale(distance_matrix, eig = TRUE, x.ret = TRUE)

# Calculate the variance percentages of the multidimensional scaling
mds_var_per <- round(mds_values$eig / sum(mds_values$eig) * 100, 1)

# Print the variance percentages of the multidimensional scaling
print(mds_var_per)

# Format the data from multidimensional scaling to optimise for ggplot
mds_points <- mds_values$points

mds_data <- data.frame(
  Sample = rownames(mds_points),
  X = mds_points[, 1],
  Y = mds_points[, 2]
)

# Print formatted data from multidimensional scaling
print(mds_data)

# Plot the multidimensiomal scaling components of the data
mds_plot <- ggplot(
  data = mds_data,
  aes(x = X, y = Y, label = Sample)
) +
  geom_text() +
  theme_bw() +
  xlab(paste("MDS1 - ", mds_var_per[1], "%", sep = "")) +
  ylab(paste("MDS2 - ", mds_var_per[2], "%", sep = "")) +
  ggtitle("MDS plot using Euclidean distance")

print(mds_plot)

# Save the plot as a .png image
file_name_2 <- "/mds-plot-1.png"
file_path_2 <- paste(
  current_directory_name,
  file_name_2,
  sep = ""
)
dev.copy(png, file = file_path_2)
dev.off()

# Calculate the binary logarithms of the initial data's matrix
log2_data_matrix <- log2(data_matrix)

# Create a second distance matrix for the data, using the absolute
# value of the binary logarithmic fold change of the matrix
log2_distance_matrix <- matrix(
  0,
  nrow = ncol(log2_data_matrix),
  ncol = ncol(log2_data_matrix),
  dimnames = list(colnames(log2_data_matrix), colnames(log2_data_matrix))
)

c <- ncol(log2_distance_matrix)

for (i in 1:c) {
  for (j in 1:i) {
    log2_distance_matrix[i, j] <-
      mean(abs(log2_data_matrix[, i] - log2_data_matrix[, j]))
  }
}

# Print the second distance matrix
print(log2_distance_matrix)

# Apply multidimentional scaling to the second distance matrix
mds_values <- cmdscale(
  as.dist(log2_distance_matrix),
  eig = TRUE,
  x.ret = TRUE
)

# Calculate the variance percentages of the multidimensional scaling
mds_var_per <- round(mds_values$eig / sum(mds_values$eig) * 100, 1)

# Print the variance percentages of the multidimensional scaling
print(mds_var_per)

# Format the data from multidimensional scaling to optimise for ggplot
mds_points <- mds_values$points

mds_data <- data.frame(
  Sample = rownames(mds_points),
  X = mds_points[, 1],
  Y = mds_points[, 2]
)

# Print formatted data from multidimensional scaling
print(mds_data)

# Plot the multidimensiomal scaling components
# of the data using the second distance matrix
mds_plot <- ggplot(
  data = mds_data,
  aes(x = X, y = Y, label = Sample)
) +
  geom_text() +
  theme_bw() +
  xlab(paste("MDS1 - ", mds_var_per[1], "%", sep = "")) +
  ylab(paste("MDS2 - ", mds_var_per[2], "%", sep = "")) +
  ggtitle("MDS plot using average log fold change as the distance")

print(mds_plot)

# Save the plot as a .png image
file_name_3 <- "/mds-plot-2.png"
file_path_3 <- paste(
  current_directory_name,
  file_name_3,
  sep = ""
)
dev.copy(png, file = file_path_3)
dev.off()