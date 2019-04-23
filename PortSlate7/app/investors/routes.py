from app.investors import blueprint
from flask import render_template
from flask_login import login_required


@blueprint.route('/')
@login_required
def investors():
 
    return render_template('investors/investors.html')

@blueprint.route('/<int:investor_id>', methods=['GET'])
@login_required
def investor(investor_id):

    return render_template('investors/investor.html', investorID=investor_id)