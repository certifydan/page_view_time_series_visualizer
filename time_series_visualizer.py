import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from datetime import datetime
from calendar import month_name
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=['date'], infer_datetime_format=True)

# Clean data
df = df.loc[(df['value'] >= df['value'].quantile(0.025))
                & (df['value'] <= df['value'].quantile(0.975))
]

def draw_line_plot():
    # Draw line plot
    df_line = df.copy()
    ax = df_line.plot(y='value', 
    use_index=True, 
    figsize=(16,6),
    xlabel='Date', 
    ylabel='Page Views', 
    title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019',
    legend=False,
    color={'value': 'red'})
    #ax.set(xlabel='Date', ylabel='Page Views', title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    fig = ax.get_figure()


    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    months = month_name[1:]
    df_bar['months'] = pd.Categorical(df_bar.index.strftime('%B'), categories=months, ordered=True)

    #df_bar = df.copy().groupby([df.index.year, df.index.strftime("%B")]).agg(average_views=('value', 'mean'))
    df_bar_p = df_bar.pivot_table(index=df_bar.index.year, columns='months', values='value')

    #df_bar = df_bar.reset_index(names=['year', 'month'])
 
    # Draw bar plot
    ax = df_bar_p.plot(kind='bar', figsize=(12,12), xlabel='Years', ylabel="Average Page Views")
    fig = ax.get_figure() 

   
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,6))

    sns.boxplot(x=df_box['year'], y=df_box['value'], ax=ax1)
    sns.boxplot(ax=ax2, x=df_box['month'], y=df_box['value'], 
    order=[
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ])

    ax1.set(xlabel='Year', ylabel='Page Views', title='Year-wise Box Plot (Trend)')
    ax2.set(xlabel='Month', ylabel='Page Views', title='Month-wise Box Plot (Seasonality)')


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
