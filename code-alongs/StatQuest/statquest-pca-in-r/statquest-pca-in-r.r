# Load packages
library(ggplot2)
library(cowplot)
library(rstudioapi)

# Get the file path of the current script:
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
  wt_values = rpois(5, lambda = sample(x = 10:1000, size = 1))
  ko_values = rpois(5, lambda = sample(x = 10:1000, size = 1))
  data_matrix[i,] <- c(wt_values, ko_values)
}

# Print the head of the matrix
print(head(data_matrix))

# Perform Principal Component Analysis (PCA) on the matrix
pca <- prcomp(t(data_matrix), scale = TRUE)

# Plot the first two principal components of the matrix
plot(pca$x[, 1], pca$x[, 2])

# Save the plot as a .png image
file_name_1 <- "/pca-plot-1.png"
file_path_1 <- paste(
  current_directory_name,
  file_name_1,
  sep = ""
)
dev.copy(png, file = file_path_1)
dev.off()

# Generate a scree plot of the matrix's principal components
pca_var <- pca$sdev^2
pca_var_per <- round(pca_var / sum(pca_var) * 100, 1)
barplot(
  pca_var_per, main = "Scree Plot",
  xlab = "Principal Component",
  ylab = "Percent Variation"
)

# Save the plot as a .png image
file_name_2 <- "/pca-plot-2.png"
file_path_2 <- paste(
  current_directory_name,
  file_name_2,
  sep = ""
)
dev.copy(png, file = file_path_2)
dev.off()

# Create a dataframe to prepare the data for ggplot2
pca_data <- data.frame(
  Sample = rownames(pca$x),
  X = pca$x[, 1],
  Y = pca$x[, 2]
)

# Print the first few rows of the dataframe
print(head(pca_data))

# Plot the first two principal components of the dataset, in variance percentage
pca_plot <- ggplot(data = pca_data, aes(x = X, y = Y, label = Sample)) +
  geom_text() +
  xlab(paste("PC1 - ", pca_var_per[1], "%", sep = "")) +
  ylab(paste("PC2 - ", pca_var_per[2], "%", sep = "")) +
  theme_bw() +
  ggtitle("My PCA Graph")
print(pca_plot)


# Save the plot as a .png image
file_name_3 <- "/my-pca-graph.png"
file_path_3 <- paste(
  current_directory_name,
  file_name_3,
  sep = ""
)
ggsave(filename = file_path_3)


# Compute and display the loading scores of the Principal Component Analysis
loading_scores <- pca$rotation[,1]
gene_scores <- abs(loading_scores)
gene_scores_ranked <- sort(gene_scores, decreasing = TRUE)
top_10_genes <- names(gene_scores_ranked[1:10])
print(top_10_genes)
top_10_genes_scores <- pca$rotation[top_10_genes, 1]
print(top_10_genes_scores)