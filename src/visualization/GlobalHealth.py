# Mar 06, 2020 - Babak J.Fard
# The code for creating time series plots and global animated map of corona virus spread
#
import numpy as np

import geopandas as gpd
import pandas as pd
from functools import reduce



#### Part 1 : Preparing the data

# 1.1 Downloading csv into dataframe
df_confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')
df_deaths = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv')
df_recovered = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv')

# 1.2 Tidying the data
# practice melt command in pandas (similar to gather in tidyr)
id_list = df_confirmed.columns.to_list()[:4]
vars_list = df_confirmed.columns.to_list()[4:]

confirmed_tidy = pd.melt(df_confirmed, id_vars=id_list, value_vars=vars_list, var_name='Date', value_name='Confirmed')
deaths_tidy = pd.melt(df_deaths, id_vars=id_list, value_vars=vars_list, var_name='Date', value_name='Deaths')
recovered_tidy = pd.melt(df_recovered, id_vars=id_list, value_vars=vars_list, var_name='Date', value_name='recovered')


# 1.3 Merging the three dataframes into one
data_frames = [confirmed_tidy, deaths_tidy, recovered_tidy]          
df_corona = reduce(lambda left, right: pd.merge(left, right, on = id_list+['Date'], how='outer'), data_frames)

# 1.4 Tidy it more. Each row only representing one observation
id_vars = df_corona.columns[:5]
data_type = ['Confirmed', 'Deaths', 'recovered']
df_corona = pd.melt(df_corona, id_vars=id_vars, value_vars=data_type, var_name='type', value_name='Count')
df_corona['Date'] = pd.to_datetime(df_corona['Date'], format='%m/%d/%y', errors='raise')
##### End. The tidy dataaframe is ready now!

# Grouping the data
# Babak : The next few line will be for the future, that I have more time to generalize it!
# groups = ['USA', 'Mainland China']
# df_corona_by_group = {}
# for a_group in groups:
#     dict[a_group] = df_corona[df_corona['Country/Region']==a_group].groupby()

USA = df_corona[df_corona['Country/Region']=='US'].groupby(['type', 'Date'], as_index=False).agg({'Count':'sum'})
ROW = df_corona[df_corona['Country/Region']!='US'].groupby(['type', 'Date'], as_index=False).agg({'Count':'sum'})
# Le's group the data into US, Mainland China, and ROW
#china = df_corona[df_corona['Count']]

#############################################################
##### Part 2. plotting the Timeseries using Plotly Express
import plotly_express as px
import plotly.io as pio 

# plot time series
# Very useful link for solving the 'type=' in legend labels:
# https://github.com/plotly/plotly_express/issues/36
def plot_timeseries(df):
    fig = px.line(df, x='Date', y='Count', color='type', template='plotly_dark', 
    color_discrete_sequence=['yellow', 'red', 'green'])\
    .for_each_trace(lambda t: t.update(name=t.name.split("=")[1]))
    #fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_layout(legend_orientation="h")
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='')
    fig.show()
    return(fig)

fig_USA = plot_timeseries(USA)
fig_ROW = plot_timeseries(ROW)
pio.write_html(fig_USA, file='/Users/babak.jfard/BabaksPage/public/2020/03/USA/index.html', auto_open=True)
pio.write_html(fig_ROW, file='/Users/babak.jfard/BabaksPage/public/2020/03/ROW/index.html', auto_open=True)


#################
### Part 3. Generate Html file for the plotly visualization


################
### Part 4. 
test = df_corona
test['Date'] = test['Date'].astype(str)
test2=test[test['type']=='Confirmed']
#classifier = mc.FisherJenks(test2.Count, k=6)
to_Category = pd.cut(test2['Count'], [-1,0,105, 361, 760, 1350, 6280, 70000], labels=[0, 1, 8, 25, 40, 60, 100])
test2 = test2.assign(size=to_Category)

fig_time= px.scatter_mapbox(data_frame=test2, lat='Lat', lon='Long',
hover_name= 'Country/Region', hover_data=['Province/State', 'Count'], size='size', animation_frame='Date', mapbox_style='stamen-toner',template='plotly_dark', zoom=1, size_max=70)
#fig_time.show()

# Saving into HTML
import plotly.io as pio
pio.write_html(fig_time, file='/Users/babak.jfard/BabaksPage/public/2020/03/animation/index.html', auto_open=True)

