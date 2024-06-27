# CREDIT:
# StatQuest: PCA in Python (published on Monday 08 January 2018)
# URL: https://www.youtube.com/watch?v=Lsue2gEM9D0

# Load packages
import random as rd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
from sklearn.decomposition import PCA

# Set a random seed value for code reproducibility
np.random.seed(30)

# Set the plot aesthetics
palette = sns.color_palette("viridis_r", as_cmap=True)
sns.set_style(style = "whitegrid", rc = {"font.family":"Times New Roman", "font.weight":"bold"})

# Create the labels for the dataset
genes = [f"gene_{i}" for i in range(1, 101)]
wt = [f"wt_{i}" for i in range(1, 6)]
ko = [f"ko_{i}" for i in range(1, 6)]

# Create a dataframe with labeled columns and rows
data = pd.DataFrame(columns = wt + ko, index = genes)

# Define the entries of the dataframe
for gene in data.index:
    data.loc[gene, "wt_1":"wt_5"] = np.random.poisson(lam = rd.randrange(10, 1000), size = 5)
    data.loc[gene, "ko_1":"ko_5"] = np.random.poisson(lam = rd.randrange(10, 1000), size = 5)

# Print the head of the dataframe
print(data.head())

# Print the shape of the dataframe
print(data.shape)

# Scale the dataframe
scaled_data = preprocessing.scale(data.T)

# Apply Principal Component Analysis (PCA) to the dataframe
pca = PCA()
pca.fit(scaled_data)
pca_data = pca.transform(scaled_data)

# Retrieve the explained variances of the dataframe's principal components
per_var = np.round(pca.explained_variance_ratio_ * 100, decimals = 1)

# Label the dataframe's principal components in descending order of the explained variance
labels = [f"PC_{i}" for i in range(1, len(per_var) + 1)]

# Plot the scree plot
plt.figure(figsize = (10, 6), dpi = 100)
plt.bar(x = range(1, len(per_var) + 1), height = per_var, tick_label = labels)
plt.xlabel("Principal Component")
plt.ylabel("Percentage of Explained Variance")
plt.title("Scree Plot")
plt.show()

# Plot the first two principal components of the dataframe
plt.figure(figsize = (10, 6), dpi = 100)
pca_df = pd.DataFrame(pca_data, index = wt + ko, columns = labels)
plt.scatter(pca_df["PC_1"], pca_df["PC_2"])
plt.xlabel(f"PC_1 - {per_var[0]}%")
plt.ylabel(f"PC_2 - {per_var[1]}%")
plt.title("My PCA Graph")
for sample in pca_df.index:
    plt.annotate(sample, (pca_df["PC_1"].loc[sample], pca_df["PC_2"].loc[sample]))
plt.show()

# Print the top ten loading scores of the genes
loading_scores = pd.Series(pca.components_[0], index = genes)
sorted_loading_scores = loading_scores.abs().sort_values(ascending = False)
top_10_genes = sorted_loading_scores[0:10].index.values
print(loading_scores[top_10_genes])