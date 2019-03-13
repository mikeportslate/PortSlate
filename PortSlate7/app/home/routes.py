
from flask import jsonify, render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from app import db, login_manager
from app.home import blueprint

@blueprint.route('/')
@blueprint.route('/index')
@login_required
def index():
 
    return render_template('home/index.html')
