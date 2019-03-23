import sqlalchemy
import pandas as pd
import datetime
import json
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://mikelam:12345678@awssample1.cji0zdy5khnh.us-west-2.rds.amazonaws.com:3306/PortSlate')
engine.connect
conn = engine.connect()

data = pd.read_sql_query('select * from v_TimeSeries', conn)
