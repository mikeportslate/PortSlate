from bcrypt import checkpw
from flask import jsonify, render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from app import db, login_manager
from app.models import User, UserMessage
from app.auth import blueprint
from app.auth.forms import LoginForm, CreateAccountForm, SubmitMessage


@blueprint.route('/')
def route_default():
    
    usermessage = SubmitMessage(request.form)
    return render_template('landing.html', usermessage=usermessage)

@blueprint.route('/page_<error>')
def route_errors(error):
    return render_template('errors/page_{}.html'.format(error))

## Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():

    login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    if 'login' in request.form and login_form.validate_on_submit():
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and checkpw(password.encode('utf8'), user.password):
            login_user(user)
            return redirect(url_for('home_blueprint.index'))
        return render_template('errors/page_403.html')
    if not current_user.is_authenticated:
        return render_template('login/login.html', login_form=login_form, create_account_form=create_account_form)

    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/create_user', methods=['POST'])
def create_user():

    create_account_form = CreateAccountForm(request.form)

    if create_account_form.validate_on_submit():
        user = User(email=create_account_form.email.data,
                                firstname=create_account_form.first_name.data,
                                lastname=create_account_form.last_name.data,
                                company=create_account_form.company.data,
                                password=create_account_form.password.data)
        db.session.add(user)
        db.session.commit()
        return jsonify ('success')

    # load registration template
    return render_template('login/login.html', login_form=login_form, create_account_form=create_account_form)

@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_blueprint.login'))


@blueprint.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

@blueprint.route('/submit_message', methods=['POST'])
def submit_message():

    submit_message_form = SubmitMessage(request.form)

    if submit_message_form.validate_on_submit():
        usermessage = UserMessage(name=submit_message_form.name.data,
                                    email=submit_message_form.email.data,
                                    subject=submit_message_form.subject.data,
                                    message=submit_message_form.message.data)
        db.session.add(usermessage)
        db.session.commit()
        return jsonify ('Message Received!')
    

## Errors


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('errors/page_403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/page_403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('errors/page_404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('errors/page_500.html'), 500
