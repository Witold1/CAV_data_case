import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import july
# import plotly.express as px

def plot_hists(df_aux, title=None, bins=30, ylims=(None, None), xlims=(None, None),
               xlabel=None, ylabel='Frequency'):
    '''
    Prepare small general purpose hists. Returns ax object
    '''
    ax = df_aux.plot.hist(bins=bins, rwidth=0.85, edgecolor='white')

    ax.set_xlim(xlims) # ax.margins(x=0.01) instead
    ax.set_ylim(ylims) # ax.margins(y=0.01) instead
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    ax.set_title(title, pad=-0.2)

    plt.tight_layout()
    return ax

def plot_calendar(df_aux, title, num_month):
    '''

    '''
    fig, ax = plt.subplots(1, num_month, figsize=(10, 5))

    for indx in range(0, num_month):
        july.month_plot(data=df_aux.values, dates=df_aux.index, month=6 + indx,
                weeknum_label=True, value_label=True, ax=ax[indx]) # , cmap="gray_r"

    fig.suptitle(title, x=0.05, horizontalalignment='left')
    fig.tight_layout(rect=[0, 0.00, 1.5, 1.])

def plot_parallel_coordinates(df_aux, title, class_column, xlabel='Week', ylabel=None, xlim=(None, None), ylim=(None, None)):
    '''
    Plots paraller coordinates chart.

    This chart is close to lineplots visually (i.e. sns.lineplot),
        but has different idea dedicated to better show ranking first
        (so, closer to a slope chart or ranking order chart)

    https://pandas.pydata.org/docs/reference/api/pandas.plotting.parallel_coordinates.html
    https://python-graph-gallery.com/parallel-plot/
    https://www.machinelearningplus.com/plots/top-50-matplotlib-visualizations-the-master-plots-python/#18.-Slope-Chart

    '''
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))

    ax.grid(which='major', axis='both', linestyle='--', alpha=0.2, zorder=1)

    pd.plotting.parallel_coordinates(frame=df_aux,
                                     class_column=class_column, axvlines_kwds={'alpha':0.5},
                                     ax=ax, zorder=10) # colormap=plt.cm.Greys
    #ax.hlines(y=40, xmin=-1, xmax=15, color='black', zorder=2)

    ax.hlines(y=df_aux.median().median(), xmin=-1, xmax=15, color='black', linestyle='dashed',
              label='median', zorder=2)

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.suptitle(title, x=0.05, horizontalalignment='left')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    #ax.legend()

    plt.tight_layout(rect=[0, 0.00, 1.5, 1.])

def plot_testing_trends(df_aux):
    '''

    '''
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    ax.grid(which='major', axis='both', linestyle='--', alpha=0.2, zorder=1)

    ax.bar(height=df_aux['TEST_ID_x'], x=df_aux.index.to_timestamp(), edgecolor='white', label='# tests')

    ax2 = ax.twinx()
    ax2.plot(df_aux.index.to_timestamp(), df_aux['TEST_ID_y'], zorder=2,
             color='red', marker='', linestyle='dashed', label='# tests per week')

    ax.set_xlabel('Date')
    ax.set_ylabel('Tests, #')

    ax2.set_ylim((0, df_aux['TEST_ID_y'].max() + 10))
    #for label in ax.get_xaxis().get_ticklabels()[::10]:
    #    label.set_visible(False)
    # https://stackoverflow.com/questions/30133280/pandas-bar-plot-changes-date-format
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))

    fig.legend(loc='right', bbox_to_anchor=(1.45, 0.03),
              ncol=3, fancybox=False, shadow=False)
    fig.tight_layout(rect=[0, 0.00, 1.5, 1.])

def plot_timely_activity(df_aux, precision='s', interval_range=None):
    '''
    Plots many bar charts in effective way
    '''
    fig, ax = plt.subplots(1, 1, figsize=(15, 8))
    ax.grid(which='major', axis='both', linestyle='--', alpha=0.2, zorder=1)

    if precision == 'h':
        ax.bar(height=df_aux, x=range(0, 24), alpha=0.9, width=0.9, edgecolor='white', zorder=2)
    elif precision == 'm':
        ax.vlines(x=range(0, 24 * 60), ymin=0, ymax=df_aux, linewidth=0.5)
    elif precision == 's':
        ax.vlines(x=range(0, 24 * 60 * 60), ymin=0, ymax=df_aux, linewidth=0.15, alpha=0.5)

    plt.xticks(ticks = range(0, interval_range, int(interval_range / 24)),
           labels = range(0, 24, 1),
           rotation = 'horizontal')
    ax.set_xlabel('Hour')
    ax.set_ylabel('Active Tests, #')

    fig.tight_layout()
