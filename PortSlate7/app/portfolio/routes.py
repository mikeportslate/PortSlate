import pandas as pd
from flask import flash, render_template, json, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from sqlalchemy import create_engine

from app import db, ma, login_manager
from app.models import User, UserSchema, LoanAbstract, LoanAbstractSchema
from app.portfolio import blueprint
from app.api.forms import LoanAbstractForm


@blueprint.route('/assets', methods=['GET','POST'])
@login_required
def portfolio_homepage():

    return render_template('portfolio/assets.html')

@blueprint.route('/asset/<int:assetid>/<asofdate>', methods=['GET','POST'])
@login_required
def portfolio_assetdetail(assetid, asofdate):

    conn = db.engine.connect()

    sql = f"select * from v_VehicleAssetList where AssetID={assetid} and Period='{asofdate}'"
    data = pd.read_sql_query(sql, conn)
    data_json = data.to_json(orient='records',date_format='iso')
    data_json=json.loads(data_json)
    

    return render_template('portfolio/asset.html', AssetSummary=data_json)


