!pip install pandas
!pip install sqlalchemy
!pip install pymysql
!pip install geopy

import sqlalchemy
import pandas as pd
import datetime
import json
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://mikelam:12345678@awssample1.cji0zdy5khnh.us-west-2.rds.amazonaws.com:3306/PortSlate')
engine.connect
conn = engine.connect()
conn.execute('select * from v_TimeSeries')

period_now = datetime.date(2019,1,31) + pd.DateOffset(months=0)
period_then = period_now - pd.DateOffset(months=12)

data = pd.read_sql_query('select * from v_TimeSeries', conn)
data.loc[data['date_maturityext_1'].isna(),'date_maturityext_1']= data.loc[data['date_maturityext_1'].isna(),'date_maturityinitial']
idx_LM=((data['Period']<=period_now) & (data['Period']>=period_now))
idx_LTM=((data['Period']<=period_now) & (data['Period']>period_then))
idx_Inception=(data['Period']<=period_now)

data_aggM =data.groupby('Period').sum()
data_aggM=data_aggM.reset_index()
data_aggM['LTV'] = data_aggM['Balance_End'] / data_aggM['MarketValue']
data_aggM['DSCR'] = data_aggM['NOI']/data_aggM['DebtService']
data_aggM['DSCR_IO']=data_aggM['NOI']/data_aggM['InterestPmt']

PortStat = { 
    "Period": period_now.strftime("%m/%d/%Y"),
    "MarketValue":data['MarketValue'][idx_LM].sum(),
    "LoanBalance":data['Balance_End'][idx_LM].sum(),
    "Cost":data['Cost'][idx_LM].sum(),
    "NAV": data['NAV'][idx_LM].sum(),
    "LTV": data['Balance_End'][idx_LM].sum()/data['MarketValue'][idx_LM].sum(),
    "LTC": data['Balance_End'][idx_LM].sum()/data['Cost'][idx_LM].sum(),
    "InterestPmt":data['InterestPmt'][idx_Inception].sum(),
    "PrincipalPmt":data['PrincipalPmt'][idx_Inception].sum(),
    "DebtService":data['DebtService'][idx_Inception].sum(),
    "DSCRIO": data['NOI'][idx_Inception].sum()/data['InterestPmt'][idx_Inception].sum(),
    "DSCR": data['NOI'][idx_Inception].sum()/data['DebtService'][idx_Inception].sum(),
    "DebtYield": data['NOI'][idx_Inception].sum()/data['Balance_End'][idx_Inception].sum()*12*100,
    "EffectRate":(data['InterestPmt'][idx_Inception].sum()/data['Balance_End'][idx_Inception].sum())*12*100,
    "EffectRate_Floating": (data['InterestPmt'][(idx_Inception) & (data['ratetype']=='Floating')].sum()/data['Balance_End'][(idx_Inception) & (data['ratetype']=='Floating')].sum())*12*100,
    "EffectRate_Fixed": (data['InterestPmt'][(idx_Inception) & (data['ratetype']=='Fixed')].sum()/data['Balance_End'][(idx_Inception) & (data['ratetype']=='Fixed')].sum())*12*100,
    "Loans_Fixed":data['Balance_End'][idx_LM & (data['ratetype']=='Fixed')].sum() / data['Balance_End'][idx_LM].sum(),
    "Loans_Floating_Cap":data['Balance_End'][idx_LM & (data['ratetype']=='Floating') & (data['interestrate_protection']==1)].sum() / data['Balance_End'][idx_LM].sum(),
    "Loans_Floating_NoCap":data['Balance_End'][idx_LM & (data['ratetype']=='Floating') & (data['interestrate_protection']==0)].sum() / data['Balance_End'][idx_LM].sum(),
    "LoanSpread": (data['indexspread'][idx_LM & (data['ratetype']=='Floating')]*data['Balance_End'][idx_LM & (data['ratetype']=='Floating')]).sum()/data['Balance_End'][idx_LM & (data['ratetype']=='Floating')].sum()
}

LineChart_json=data_aggM.loc[data_aggM['Period']<=period_now, ['Period','MarketValue','NAV','LTV', 'InterestPmt','PrincipalPmt','DebtService','DSCR','DSCR_IO']]
LineChart_json=LineChart_json.to_json(orient='columns', date_format='iso')
LineChart_json=json.loads(LineChart_json)

BarChart=data.loc[data['Period']==data['date_maturityinitial']]
BarChartInitial=BarChart.groupby(lambda x: BarChart['date_maturityinitial'][x].year).sum()
BarChartInitial['Year']=BarChartInitial.index
BarChartInitial_json=BarChartInitial[['Year','Balance_End']]
BarChartInitial_json=BarChartInitial_json.to_json(orient='records', date_format='iso')
BarChartInitial_json=json.loads(BarChartInitial_json)

BarChart=data.loc[data['Period']==data['date_maturityext_1']]
BarChartExt=BarChart.groupby(lambda x: BarChart['date_maturityext_1'][x].year).sum()
BarChartExt['Year']=BarChartExt.index
BarChartExt_json=BarChartExt[['Year','Balance_End']]
BarChartExt_json=BarChartExt_json.to_json(orient='records', date_format='iso')
BarChartExt_json=json.loads(BarChartExt_json)

year = BarChartExt['Year'].max()
years=list(range(year-3, year+2, 1))
maturityInitial_json = {};
maturityExt_json = {};
for i in years:
    row = {str(i): pd.to_numeric(BarChartInitial[BarChartInitial['Year']==i]['Balance_End'].sum())}
    maturityInitial_json.update(row)
    row = {str(i): pd.to_numeric(BarChartExt[BarChartExt['Year']==i]['Balance_End'].sum())}
    maturityExt_json.update(row)
