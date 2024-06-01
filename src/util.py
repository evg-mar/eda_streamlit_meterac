import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer, get_streamlit_html

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np 
import pandas as pd

def corrdot(*args, **kwargs):
    corr_r = args[0].corr(args[1], 'pearson')
    corr_text = f"{corr_r:2.2f}".replace("0.", ".")
    ax = plt.gca()
    ax.set_axis_off()
    marker_size = abs(corr_r) * 10000
    ax.scatter([.5], [.5], marker_size, [corr_r], alpha=0.6, cmap="coolwarm",
            vmin=-1, vmax=1, transform=ax.transAxes)
    font_size = abs(corr_r) * 40 + 5
    ax.annotate(corr_text, [.5, .5,],  xycoords="axes fraction",
                ha='center', va='center', fontsize=font_size)

def plot_corr(data_df: pd.DataFrame, year_option, month_n_hour_option, agg_function):
    sns.set_theme(style='white', font_scale=1.6)
    df_ = data_df[data_df['year']==int(year_option)][[month_n_hour_option, 
                                        'pm_2.5', 
                                        'pm_10.0', 
                                        'humidity', 
                                        'temperature']].groupby(month_n_hour_option).agg(agg_function)
    # df_['month_3h']
    # df_
    g = sns.PairGrid(df_, aspect=1.4, diag_sharey=False)
    g.map_lower(sns.regplot, lowess=True, ci=False, line_kws={'color': 'black'})
    g.map_diag(sns.distplot, kde_kws={'color': 'black'})
    g.map_upper(corrdot)
    # g.figure.set_size_inches(10,10)
    st.pyplot(g)


@st.cache_data(experimental_allow_widgets=True)
def preprocess_df(file_path:str) -> pd.DataFrame:
    """
    Preprocess dataframe and introduce additional useful columns
    """
    df = pd.read_csv(file_path)
    col_datetime_str = 'datetime' if 'datetime' in df.columns else 'Date/Time'

    df['datetime'] = pd.to_datetime(df[col_datetime_str])
    if 'Date/Time' in df.columns:
        del df['Date/Time']
    df['3hour'] = df.datetime.dt.round('3h').dt.hour
    df['6hour'] = df.datetime.dt.round('6h').dt.hour

    df['year'] = df['datetime'].dt.year 
    df['month'] = df['datetime'].dt.month 
    df['day'] = df['datetime'].dt.day
    df['hour'] = df['datetime'].dt.hour
    df['year_month_hour'] = df.apply(lambda row: str(row['year']) + '-' +  \
                                     str(row['month']).zfill(2) + '-' + \
                                        str(row['hour']).zfill(2) , axis=1)
    df['month_hour'] = df.apply(lambda row: str(row['month']).zfill(2) + '-' + \
                                str(row['hour']).zfill(2) , axis=1)
    df['year_month_3hour'] = df.apply(lambda row: str(row['year']) + '-' +  \
                                      str(row['month']).zfill(2) + '-' + \
                                        str(row['3hour']).zfill(2) , axis=1)
    df['month_3hour'] = df.apply(lambda row: str(row['month']).zfill(2) + '-' + \
                                 str(row['3hour']).zfill(2) , axis=1)
    df['year_month_6hour'] = df.apply(lambda row: str(row['year']) + '-' +  \
                                      str(row['month']).zfill(2) + '-' + \
                                        str(row['6hour']).zfill(2) , axis=1)
    df['month_6hour'] = df.apply(lambda row: str(row['month']).zfill(2) + '-' + \
                                 str(row['6hour']).zfill(2) , axis=1)

    df['pm_2.5'] = np.minimum(df['pm_2.5'].to_numpy(), np.array([500.]*len(df)))
    df['pm_10.0'] = np.minimum(df['pm_10.0'].to_numpy(), np.array([500.]*len(df)))

    return df
# df

@st.cache_resource
def get_pyg_html(df: pd.DataFrame) -> str:
    # When you need to publish your application, you need set `debug=False`,
    #prevent other users to write your config file.
    html = get_streamlit_html(df, use_kernel_calc=True, 
                              spec="./config_pygwalk.json", 
                              debug=False)
    return html

# You should cache your pygwalker renderer, if you don't want your memory to explode
@st.cache_resource
def get_pyg_renderer(df: pd.DataFrame) -> "StreamlitRenderer":
    # df = preprocess_df(file_path=file_path)
    # When you need to publish your application, you need set 
    # `debug=False`,prevent other users to write your config file.
    return StreamlitRenderer(df,  use_kernel_calc=True, 
                             spec="./config_pygwalk.json", 
                             debug=False)
