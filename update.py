import pandas as pd
import datetime as dt
# Portwatch
data = pd.read_csv('https://opendata.arcgis.com/api/v3/datasets/42132aa4e2fc4d41bdaf9a445f688931_0/downloads/data?format=csv&spatialRefId=4326&where=1=1')
data['datetime'] = pd.to_datetime(data['date'], format='mixed')
data['datetime'] = data['datetime'].dt.strftime('%Y-%m-%d')
output = data[['portname','datetime','n_total','capacity']]
flourish = output.pivot(index='datetime', columns='portname', values='capacity')
flourish = flourish.sort_index()
flourish = flourish.div(1000000)
flourish = flourish.rolling(window=7).mean()
flourish.index = pd.to_datetime(flourish.index, format='%Y-%m-%d')  # Example format
flourish_weekly = flourish.resample('W-SUN').bfill()
flourish_weekly = flourish_weekly.assign(index_copy=flourish_weekly.index)
flourish_weekly['Month'] = flourish_weekly['index_copy'].dt.strftime('%b %d, %Y')
flourish_weekly.to_csv('output_w.csv')
