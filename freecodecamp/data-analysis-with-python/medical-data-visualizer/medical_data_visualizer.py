import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("medical_examination.csv")

# Add 'overweight' column
df['overweight'] = ((df["weight"] / ((df["height"] / 100) ** 2)) > 25).apply(int)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df["cholesterol"] = (df["cholesterol"] > 1).apply(int)
df["gluc"] = (df["gluc"] > 1).apply(int)

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars = "cardio", value_vars = ["cholesterol", "gluc", "smoke", "alco", "active", "overweight"])


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = df_cat.groupby(["cardio", "variable"]).value_counts().reset_index()
    df_cat.columns = ["cardio", "variable", "value", "total"]

    # Draw the catplot with 'sns.catplot()'
    plot = sns.catplot(data = df_cat, x = "variable", y = "total", hue = "value", col = "cardio", kind = "bar")


    # Get the figure for the output
    fig = plot.fig


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[
            (df["ap_lo"] <= df["ap_hi"]) 
        &   (df["weight"] >= df["weight"].quantile(0.025))
        &   (df["weight"] <= df["weight"].quantile(0.975))
        &   (df["height"] >= df["height"].quantile(0.025))
        &   (df["height"] <= df["height"].quantile(0.975))
    ]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    ### BEGINNING OF CREDIT ###
    # Source : https://www.geeksforgeeks.org/how-to-create-a-triangle-correlation-heatmap-in-seaborn-python/
    # Author : https://auth.geeksforgeeks.org/user/vanshikagoyal43/articles?utm_source=geeksforgeeks&utm_medium=article_author&utm_campaign=auth_user
    mask = np.triu(np.ones_like(corr))
    ### END OF CREDIT

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize = (16, 9), dpi = 300)

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(data = corr, annot = True, linewidths = 0.75, square = True, fmt="0.1f", mask = mask, cmap = "viridis")


    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
