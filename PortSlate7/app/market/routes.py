from app.market import blueprint
from flask import render_template
from flask_login import login_required


@blueprint.route('/competitors')
@login_required
def competitors():
 
    return render_template('market/competitors.html')

@blueprint.route('/competitor/<int:competitor_id>', methods=['GET'])
@login_required
def competitor(competitor_id):

    return render_template('market/competitor.html')