
from flask import flash, render_template, json, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from sqlalchemy import create_engine

from app import db, ma, login_manager
from app.models import User, UserSchema, LoanAbstract, LoanAbstractSchema
from app.portfolio import blueprint
from app.api.forms import LoanAbstractForm


@blueprint.route('/assets', methods=['GET'])
@login_required
def portfolio_homepage():

    return render_template('portfolio/assets.html')

@blueprint.route('/asset/<int:asset_id>', methods=['GET'])
@login_required
def portfolio_assetdetail(asset_id):

    return render_template('portfolio/asset.html')


