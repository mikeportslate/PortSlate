import sqlalchemy
import pandas as pd
import numpy as np
import datetime
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import json
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://mikelam:12345678@awssample1.cji0zdy5khnh.us-west-2.rds.amazonaws.com:3306/PortSlate')
engine.connect
conn = engine.connect()

AssetID = 3
sql = f"select * from v_AssetCF where AssetID={AssetID}"
data = pd.read_sql_query(sql, conn)
data['Year'] = data['Period'].dt.year
data_year=pd.pivot_table(data, index={'FieldDisplayName', 'DisplayOrder'}, columns='Year', values='Amount', aggfunc=np.sum)
data_year=data_year.reset_index()
data_year_json= data_year.to_json(orient='records', date_format='iso')
data_year_json=json.loads(data_year_json)
data_year_json