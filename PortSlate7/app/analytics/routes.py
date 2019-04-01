from app.analytics import blueprint
from flask import render_template
from flask_login import login_required


@blueprint.route('/fundmodel', methods=['GET','POST'])
@login_required
def fundmodel():
 
    return render_template('analytics/fundmodel.html')

@blueprint.route('/interestrate', methods=['GET','POST'])
@login_required
def interestrate():

    return render_template('analytics/interestrate.html')