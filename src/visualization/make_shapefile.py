# I have downloaded ACS 5 year estimate 2017 - Table B01001
# I have downloaded TIGER shape file of NE- BG level
import numpy as np
import pandas as pd
import geopandas as gpd 
import re

def abbreviate(word):
    #print(word)
    a1 = re.sub('[a-z]*;\s', '_', word)
    a2 = a1.replace(': - ','_')
    a3 = a2.replace(' ', '_').replace('_years', '')
    return(a3)
 
# reaiding files
shp = gpd.read_file('zip:///Users/babak.jfard/Downloads/cb_2017_31_bg_500k.zip')
df = pd.read_csv('/Users/babak.jfard/Downloads/aff_download/ACS_17_5YR_B01001_with_ann_60_Over.csv')

df.head()
cols = [c for c in df.columns if not('Margin' in c)]

df=df[cols]

# Have to simplify the names of the columns, later ArcGIS Online do not mess them up
a = df.columns.to_list()
a = [abbreviate(x) for x in a]
a = [x.replace('Male', 'M') for x in a]
a = [x.replace('Female', 'F') for x in a]
df.columns=a

shp['GEOID']=shp['GEOID'].astype('str')
df['Id2']=df['Id2'].astype('int').astype('str')
df_shp = pd.merge(shp, df, left_on='AFFGEOID', right_on='Id')

df_shp.to_file('/Users/babak.jfard/Downloads/NE_ages_Bg-2017_over60.shp')
 

