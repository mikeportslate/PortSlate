from app.market import blueprint
from flask import render_template
from flask_login import login_required


@blueprint.route('/competitor')
@login_required
def index():
 
    return render_template('market/competitor.html')
