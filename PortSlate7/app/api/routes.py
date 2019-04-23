
import pandas as pd
import datetime
from flask import flash, render_template, json, jsonify, request
from flask_login import login_required, current_user
# from datetime import datetime
from sqlalchemy.sql import text

from app import db, ma, login_manager
from app.models import User, UserSchema, LoanAbstract,LoanAbstractSchema
from app.api import blueprint
from app.api.forms import LoanAbstractForm


user_schema=UserSchema()
users_scehma=UserSchema(many=True)
loanabstract_schema=LoanAbstractSchema()
loanabstracts_schema=LoanAbstractSchema(many=True)


@blueprint.route('/asset/list', methods=['GET'])
@login_required
def api_assetList():

    loanabstract = LoanAbstract.query.from_statement(text("SELECT * FROM v_LoanAbstract"))
    loanabstractJS=loanabstracts_schema.dump(loanabstract)
    
    return jsonify({'data': loanabstractJS.data})

@blueprint.route('/asset/add', methods=['POST', 'GET'])
@login_required
def api_assetAdd():
    """
    Add a asset record
    """
    form = LoanAbstractForm()
    if form.validate_on_submit():
        loan = LoanAbstract(property=form.property.data, 
                lender=form.lender.data, 
                loantype=form.loantype.data,
                ratetype=form.ratetype.data,
                index=form.index.data,
                indexrate=form.indexrate.data,
                indexspread=form.indexspread.data,
                interestrate_initial=form.interestrate_initial.data,
                date_funding=form.date_funding.data,
                date_maturityinitial=form.date_maturityinitial.data,
                funding_total=form.funding_total.data,
                last_modified=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        try:
            # add the music record to the database
            db.session.add(loan)
            db.session.commit()
            flash('You have successfully added a new loan.')
        except:
            # in case department name already exists
            flash('Error: the song already exists.')

        return jsonify(status='OK',message='inserted successfully')

    return jsonify(success=False,message='Error 1')


@blueprint.route('/asset/add/<int:loan_id>', methods=['POST', 'GET'])
@login_required
def api_assetEdit(loan_id):
    """
    Edit existing record
    """
    form = LoanAbstractForm()
    if form.validate_on_submit():
        loanabsract = LoanAbstract.query.filter_by(id=loan_id).first()
        loanabsract.property = form.property.data
        loanabsract.lender = form.lender.data
        loanabsract.loantype = form.loantype.data
        loanabsract.ratetype = form.ratetype.data
        loanabsract.index = form.index.data
        loanabsract.indexrate = form.indexrate.data
        loanabsract.indexspread = form.indexspread.data
        loanabsract.interestrate_initial = form.interestrate_initial.data
        loanabsract.date_funding = form.date_funding.data
        loanabsract.date_maturityinitial = form.date_maturityinitial.data
        loanabsract.funding_total = form.funding_total.data.replace(",","")
        loanabsract.last_modified = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.session.commit()
        flash('Edit Successful')

        return jsonify(status='OK',message='inserted successfully')

    return jsonify(success=False,message='Error 2')

@blueprint.route('/asset/delete/<int:loan_id>', methods=['POST', 'GET'])
def api_assetDelete(loan_id):
    """
    Delete
    """
    loanabstract = LoanAbstract.query.filter_by(id=loan_id).first()
    if loanabstract: 
        db.session.delete(loanabstract)
        db.session.commit()
        flash('You have successfully deleted the Song.')

        return jsonify(status='OK',message='inserted successfully')
    
    return jsonify(success=False,message='Error')


@blueprint.route('/chart/list', methods=['GET', 'POST'])
@login_required
def api_chartlist():

    sql = text('select * from v_PortChart1')
    curr = db.engine.execute(sql)
    row_headers=[x[0] for x in curr.cursor.description] 
    rows = curr.fetchall()

    json_data=[]
    for row in rows:
        json_data.append(dict(zip(row_headers, row)))
    
    return jsonify({'data': json_data})


@blueprint.route('/dashboard/summary', methods=['GET', 'POST'])
@login_required
def api_dashSummary():

    conn = db.engine.connect()
    period_now = datetime.date(2019,1,31) + pd.DateOffset(months=0)
    period_then = period_now - pd.DateOffset(months=12)

    data = pd.read_sql_query('select * from v_TimeSeries', conn)
    data.loc[data['date_maturityext_1'].isna(),'date_maturityext_1']= data.loc[data['date_maturityext_1'].isna(),'date_maturityinitial']
    idx_LM=((data['Period']<=period_now) & (data['Period']>=period_now))
    idx_LTM=((data['Period']<=period_now) & (data['Period']>period_then))
    idx_Inception=(data['Period']<=period_now)

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
    
    return jsonify(PortStat)

@blueprint.route('/dashboard/timeseries', methods=['GET', 'POST'])
@login_required
def api_dashtimeseries():

    conn = db.engine.connect()
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

    LineChart_json=data_aggM.loc[data_aggM['Period']<=period_now, ['Period','MarketValue','NAV','LTV', 'InterestPmt','PrincipalPmt','DebtService','DSCR','DSCR_IO']]
    LineChart_json=LineChart_json.to_json(orient='columns', date_format='iso')
    LineChart_json=json.loads(LineChart_json)

    BarChart=data.loc[data['Period']==data['date_maturityinitial']]
    BarChartInitial=BarChart.groupby(lambda x: BarChart['date_maturityinitial'][x].year).sum()
    BarChartInitial['Year']=BarChartInitial.index

    BarChart=data.loc[data['Period']==data['date_maturityext_1']]
    BarChartExt=BarChart.groupby(lambda x: BarChart['date_maturityext_1'][x].year).sum()
    BarChartExt['Year']=BarChartExt.index

    year=BarChartExt['Year'].max()
    years=list(range(year-4, year+3, 1))
    MaturityInitial_json = {}
    MaturityExt_json = {}

    for i in years:
        row = {str(i): pd.to_numeric(BarChartInitial[BarChartInitial['Year']==i]['Balance_End'].sum())}
        MaturityInitial_json.update(row)
        row = {str(i): pd.to_numeric(BarChartExt[BarChartExt['Year']==i]['Balance_End'].sum())}
        MaturityExt_json.update(row)



    Output_json = {'Monthly Figures': LineChart_json, 'Maturity Initial': MaturityInitial_json, 'Maturity Extended': MaturityExt_json}

    
    return jsonify(Output_json)


@blueprint.route('/dashboard/assets', methods=['GET', 'POST'])
@login_required
def api_dashAssets():

    conn = db.engine.connect()

    vehicle = request.form['vehicle']
    asofdate = request.form['asofdate']

    sql = f"select * from v_VehicleAssetList where VehicleName='{vehicle}' and Period<='{asofdate}'"
    data = pd.read_sql_query(sql, conn)

    data_AssetGeo=data[{'VehicleName','PropertyName','lat','long','GAV_P'}]
    data_AssetGeo=data_AssetGeo.rename(columns={'PropertyName':'name'})
    data_AssetGeo_json=data_AssetGeo.to_json(orient='records')
    data_AssetGeo_json = json.loads(data_AssetGeo_json)

    data_AssetType = data[{'VehicleName','PropertyType','GAV_P'}].groupby(['VehicleName','PropertyType'])
    data_AssetRegion = data[{'VehicleName','NCREIF_Region','GAV_P'}].groupby(['VehicleName','NCREIF_Region'])
    data_AssetType=data_AssetType.sum().reset_index()
    data_AssetRegion=data_AssetRegion.sum().reset_index()
    data_AssetType_json=data_AssetType.to_json(orient='records')
    data_AssetRegion_json=data_AssetRegion.to_json(orient='records')
    data_AssetType_json = json.loads(data_AssetType_json)
    data_AssetRegion_json = json.loads(data_AssetRegion_json)

    output_json = {'geo': data_AssetGeo_json, 'assettype': data_AssetType_json, 'assetregion': data_AssetRegion_json}


    return jsonify(output_json)

@blueprint.route('/portfolio/assets', methods=['GET', 'POST'])
@login_required
def api_portfolioassets():

    conn = db.engine.connect()
    vehicle = request.form['vehicle']
    asofdate = request.form['asofdate']

    # data = pd.read_sql_query('select * from v_PortfolioAssetList', conn)
    sql = f"select * from v_VehicleAssetList where VehicleName='{vehicle}' and Period='{asofdate}'"
    data = pd.read_sql_query(sql, conn)
    data = data[{'AssetID','PropertyName','City','State','Country','PropertyType','PurchaseDate','SquareFeet','UnitNumber','Occupancy_P','P_USD_TotalCostUnlevered','GAV_P','DebtBalanceEnd','RateType','MaturityInitial','Index','IndexSpread','Img'}]
    data['NAV'] = data['GAV_P']-data['DebtBalanceEnd']
    data['LTV'] = data['DebtBalanceEnd']/data['GAV_P']
    data['AssetName'] = data['PropertyName'] + '<br>' + data['City'] + ' ' + data['State'] + ' ' + data['Country']
    data['Sqft_Unit'] = data['UnitNumber']
    data.loc[data['Sqft_Unit'].isnull(),'Sqft_Unit'] = data['SquareFeet']
    data.rename(columns={'P_USD_TotalCostUnlevered':'Cost','GAV_P':'GAV','DebtBalanceEnd':'LoanBalance','MaturityInitial':'Maturity','Occupancy_P':'Occupancy'}, inplace=True)
    data['InterestRate']= data['Index'] + ' + ' +  data['IndexSpread'].astype(str) + 'bps'

    data_json = data.to_json(orient='records')
    data_json=json.loads(data_json)

    return jsonify({'data': data_json})

@blueprint.route('/asset/irr', methods=['GET', 'POST'])
@login_required
def api_assetIRR():
    
    conn=db.engine.connect()
    exitCost = request.form['exitCost']
    exitYear = request.form['exitYear']
    exitCap = request.form['exitCap']
    exitNOIAdj = request.form['exitNOIAdj']
    exitJV = request.form['JV']
    vehicle = request.form['vehicle']
    assetID = request.form['assetID']

    exitDate = exitYear + '-12-' + '31'
    exitCost = float(exitCost.strip('%'))/100
    exitCap = float(exitCap.strip('%'))/100
    exitJV = float(exitJV.strip('%'))/100
    
    sql = f"call sp_IRRCF_Asset ('{assetID}','{vehicle}', '{exitDate}')"
    data = pd.read_sql_query(sql, conn)
    data['Year'] = data['Period'].dt.year
    data['Month'] = data['Period'].dt.month.astype(str)
    data['Month']=data['Month'].apply(lambda x: x.zfill(2))

    data_yearmonth=pd.pivot_table(data, index={'Year', 'Month'}, columns='Field', values='Amount', aggfunc=np.sum)
    data_yearmonth=data_yearmonth.reset_index()
    data_yearmonth=data_yearmonth.fillna(0).copy()

    data_yearmonth['GrossProceed']=0
    data_yearmonth['NetProceed']=0

    # data_yearmonth.to_csv('temp_yrmonth.csv')

    DebtFunding= data_yearmonth.loc[0]['GrossPurchasePrice']-data_yearmonth.loc[0]['EquityContribution']
    data_yearmonth.loc[0,'DebtFunding'] = DebtFunding
    exitIdx=((data_yearmonth['Month']=='12') & (data_yearmonth['Year']==2023))
    data_yearmonth.loc[exitIdx, 'GrossProceed']=data_yearmonth.loc[exitIdx, 'NTMNOI']/exitCap * (1-exitCost)
    data_yearmonth.loc[exitIdx,'DebtPayoff']=data_yearmonth.loc[exitIdx,'DebtBalanceEnd']
    data_yearmonth.loc[exitIdx, 'NetProceed']=data_yearmonth.loc[exitIdx, 'GrossProceed']-data_yearmonth.loc[exitIdx, 'DebtPayoff']
    data_yearmonth['CashflowUnlever']=-data_yearmonth['GrossPurchasePrice']+data_yearmonth['NETOPERATINGINCOME']+data_yearmonth['GrossProceed']
    data_yearmonth['CashflowLever']=-data_yearmonth['EquityContribution']+data_yearmonth['NETOPERATINGINCOME']+data_yearmonth['DebtService']+data_yearmonth['NetProceed']
    ReturnUnlever=((1+np.irr(data_yearmonth['CashflowUnlever']))**12) - 1
    ReturnLever=(1+np.irr(data_yearmonth['CashflowLever']))**12-1

    data_year=data_yearmonth.groupby('Year').sum().copy()
    data_year=data_year.reset_index()
    data_year['ReturnUnlever']=0
    data_year['ReturnLever']=0

    data_year.loc[0,'ReturnUnlever']=ReturnUnlever
    data_year.loc[0,'ReturnLever']=ReturnLever
    data_year_json=data_year.to_json(orient='columns', date_format='iso')
    data_year_json=json.loads(data_year_json)

    return jsonify(data_year_json)

@blueprint.route('/investors/database', methods=['GET', 'POST'])
@login_required
def api_investorsDatabase():

    conn = db.engine.connect()
    # vehicle = request.form['vehicle']
    # asofdate = request.form['asofdate']

    sql = f"call sp_InvestorDatabase ()"
    data = pd.read_sql_query(sql, conn)
 
    data_json = data.to_json(orient='records')
    data_json=json.loads(data_json)

    return jsonify({'data': data_json})


@blueprint.route('/investors/history', methods=['GET', 'POST'])
@login_required
def api_investorsHistory():

    conn = db.engine.connect()
    # vehicle = request.form['vehicle']
    # asofdate = request.form['asofdate']

    sql = f"call sp_FundingFolders ()"
    data = pd.read_sql_query(sql, conn)
 
    data_json = data.to_json(orient='records')
    data_json=json.loads(data_json)

    return jsonify({'data': data_json})

@blueprint.route('/investor/summary', methods=['POST'])
@login_required
def api_investorSummary():

    conn = db.engine.connect()
    investor = request.form['investor']

    sql = f"select * from t_ref_Investor where InvestorID={investor}"
    data = pd.read_sql_query(sql, conn)
 
    data_json = data.to_json(orient='records')
    data_json=json.loads(data_json)

    return jsonify(data_json)    

@blueprint.route('/investor/chart', methods=['POST'])
@login_required
def api_investorChart():

    conn = db.engine.connect()
    investor = request.form['investor']
    investor = int(investor)

    sql = f"call sp_InvestorAccountHistory({investor})"
    data = pd.read_sql_query(sql, conn)
    data = data.sort_values(by='FundingDate', ascending=True).copy()

    data_funding=data.loc[data['Activity']=='Capital Contribution',['FundingDate','FundingAmount']].copy()
    data_funding['CumSum']=data_funding['FundingAmount'].cumsum()

    data_dvd = data.loc[data['Activity']=='Dividend',['FundingDate', 'CurrentShares','FundingAmount']].copy()
    data_dvd['EPS'] = data_dvd['FundingAmount']/data_dvd['CurrentShares']

    data_funding_json = data_funding.to_json(orient='records' , date_format='iso')
    data_funding_json = json.loads(data_funding_json)

    data_dvd_json = data_dvd.to_json(orient='records' , date_format='iso')
    data_dvd_json = json.loads(data_dvd_json)
    
    return jsonify()

@blueprint.route('/investor/history', methods=['GET', 'POST'])
@login_required
def api_investorHistory():

    conn = db.engine.connect()
    investor = request.form['investor']
    investor = int(investor)
    

    sql = f"call sp_InvestorAccountHistory ({investor})"
    data = pd.read_sql_query(sql, conn)
 
    data_json = data.to_json(orient='records')
    data_json=json.loads(data_json)

    return jsonify({'data': data_json})
