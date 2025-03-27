import pandas as pd
import datetime as dt
# Portwatch
"""
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
"""
from fredapi import Fred
indeed_codes = ['IHLIDXUSTPACCO',
 'IHLIDXUSTPADMIASSI',
 'IHLIDXUSTPARCH',
 'IHLIDXUSTPAREN',
 'IHLIDXUSTPBAFI',
 'IHLIDXUSTPBEWE',
 'IHLIDXUSTPCHIL',
 'IHLIDXUSTPCIVIENGI',
 'IHLIDXUSTPCLSA',
 'IHLIDXUSTPCONS',
 'IHLIDXUSTPCOSOSE',
 'IHLIDXUSTPCUSTSERV',
 'IHLIDXUSTPDENT',
 'IHLIDXUSTPDRIV',
 'IHLIDXUSTPEDIN',
 'IHLIDXUSTPELECENGI',
 'IHLIDXUSTPFOPRSE',
 'IHLIDXUSTPHOTO',
 'IHLIDXUSTPHUMARESO',
 'IHLIDXUSTPINDEDO',
 'IHLIDXUSTPINDUENGI',
 'IHLIDXUSTPINMA',
 'IHLIDXUSTPINSU',
 'IHLIDXUSTPITOPHE',
 'IHLIDXUSTPLEGA',
 'IHLIDXUSTPLOGISUPP',
 'IHLIDXUSTPLOST',
 'IHLIDXUSTPMANA',
 'IHLIDXUSTPMARK',
 'IHLIDXUSTPMATH',
 'IHLIDXUSTPMECO',
 'IHLIDXUSTPMEDIINFO',
 'IHLIDXUSTPMEDITECH',
 'IHLIDXUSTPNURS',
 'IHLIDXUSTPPECAHOHE',
 'IHLIDXUSTPPHAR',
 'IHLIDXUSTPPHSU',
 'IHLIDXUSTPPRMA',
 'IHLIDXUSTPPROJMANA',
 'IHLIDXUSTPRETA',
 'IHLIDXUSTPSALE',
 'IHLIDXUSTPSCREDE',
 'IHLIDXUSTPSEPUSA',
 'IHLIDXUSTPSOFTDEVE',
 'IHLIDXUSTPSPOR',
 'IHLIDXUSTPTHER',
 'IHLIDXUSTPVETE']

import os
fred_api_key = os.getenv('FRED_API')
if fred_api_key is None:
    raise ValueError("API_KEY environment variable is not set")

fred = Fred(api_key=fred_api_key)
col_names = pd.DataFrame({series:fred.get_series_info(series) for series in indeed_codes})
col_names.head()
collist = col_names.iloc[3].tolist()
new_list = []

for item in collist:
  new_item = item.replace(" Job Postings on Indeed in the United States", "")
  new_list.append(new_item)
data = pd.DataFrame({series:fred.get_series(series) for series in indeed_codes})
data.columns = new_list
dataOut = data.copy()
dataOut['Month'] = data.index


# Convert the column to datetime format
dataOut['Month'] = pd.to_datetime(dataOut['Month'])

# Use strftime to format the date as 'Month-Year'
dataOut['Month'] = dataOut['Month'].dt.strftime('%b-%y')
# If needed select time period
#dataOut = dataOut.loc['2001-01-01':]
dataOut= dataOut.fillna(method='ffill')
dataOut = dataOut.resample('M').last()
dataOut.to_csv('indeed.csv')
