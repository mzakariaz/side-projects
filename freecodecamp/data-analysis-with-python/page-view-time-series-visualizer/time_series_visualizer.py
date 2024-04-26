import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to "date".)
df = pd.read_csv("fcc-forum-pageviews.csv")
df = df.set_index("date")
df.index = pd.to_datetime(df.index)

# Clean data
df = df.loc[(df["value"] >= df["value"].quantile(0.025)) & (df["value"] <= df["value"].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize = (16, 9), dpi = 300)
    sns.lineplot(data = df, x = df.index, y = "value").set(title = "Daily freeCodeCamp Forum Page Views 5/2016-12/2019", xlabel = "Date", ylabel = "Page Views")
    
    # Save image and return fig (don't change this part)
    fig.savefig("line_plot.png")
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar.reset_index(inplace = True)
    df_bar["year"] = [d.year for d in df_bar.date]
    df_bar["month"] = pd.Categorical([d.strftime("%B") for d in df_bar.date], categories = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], ordered = True)

    # Draw bar plot
    fig, ax = plt.subplots(figsize = (16, 9), dpi = 300)
    sns.barplot(data = df_bar, x = "year", y = "value", hue = "month").set(xlabel = "Years", ylabel = "Average Page Views", title = "Yearly/Monthly freeCodeCamp Forum Page Views 5/2016-12/2019")
    plt.legend(title = "Months", loc = "upper left")

    # Save image and return fig (don't change this part)
    fig.savefig("bar_plot.png")
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace = True)
    df_box["year"] = [d.year for d in df_box.date]
    df_box["month"] = [d.strftime("%b") for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize = (32, 18), dpi = 300)
    sns.boxplot(data = df_box, x = "year", y = "value", ax = axes[0]).set(title = "Year-wise Box Plot (Trend)", xlabel = "Year", ylabel = "Page Views")
    sns.boxplot(data = df_box, x = "month", y = "value", order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], ax = axes[1]).set(title = "Month-wise Box Plot (Seasonality)", xlabel = "Month", ylabel = "Page Views")
    
    # Save image and return fig (don't change this part)
    fig.savefig("box_plot.png")
    return fig
