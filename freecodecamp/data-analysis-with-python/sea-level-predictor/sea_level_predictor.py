import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    # Read data from file
    df = pd.read_csv("epa-sea-level.csv")

    # Create scatter plot
    fig, ax = plt.subplots(figsize = (16, 9), dpi = 300)
    plt.scatter(df["Year"], df["CSIRO Adjusted Sea Level"])

    # Create first line of best fit
    lg_1 = linregress(df["Year"], df["CSIRO Adjusted Sea Level"])
    slope_1, intercept_1 = lg_1[0], lg_1[1]
    plt.plot(pd.Series(list(range(1880, 2051))), slope_1 * pd.Series(list(range(1880, 2051))) + intercept_1)

    # Create second line of best fit
    df_2 = df.loc[df["Year"] >= 2000]
    lg_2 = linregress(df_2["Year"], df_2["CSIRO Adjusted Sea Level"])
    slope_2, intercept_2 = lg_2[0], lg_2[1]
    plt.plot(pd.Series(list(range(2000, 2051))), slope_2 * pd.Series(list(range(2000, 2051))) + intercept_2)

    # Add labels and title
    plt.xlabel("Year")
    plt.ylabel("Sea Level (inches)")
    plt.xticks([1850.0, 1875.0, 1900.0, 1925.0, 1950.0, 1975.0, 2000.0, 2025.0, 2050.0, 2075.0])
    plt.title("Rise in Sea Level")
    
    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()