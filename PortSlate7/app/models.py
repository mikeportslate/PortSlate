from bcrypt import gensalt, hashpw
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, Numeric, DateTime, DECIMAL

from app import db, login_manager, ma


class User(db.Model, UserMixin):

    __tablename__ = 't_ref_User'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    firstname=Column(String)
    lastname=Column(String)
    company=Column(String)
    password =Column(Binary)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            if property == 'password':
                value = hashpw(value.encode('utf8'), gensalt())
            setattr(self, property, value)

    def __repr__(self):
        return str(self.email)

class UserSchema(ma.Schema):
    class Meta:
        fields=('first_name', 'last_name', 'company','email')

class UserMessage(db.Model):

    __tablename__= 't_ref_Message'

    id = Column(Integer, primary_key=True)
    name= Column(String)
    email = Column(String)
    subject = Column(String)
    message = Column(String)



class LoanAbstract(db.Model):

    __tablename__ = 't_ref_LoanAbstract'

    id = db.Column(db.Integer, primary_key=True)
    property = db.Column(db.String(60), index=True, unique=True)
    lender = db.Column(db.String(60))
    loantype = db.Column(db.String(60))
    ratetype=db.Column(db.String(60))
    index=db.Column(db.String(60))
    indexrate=db.Column(db.Numeric)
    indexspread=db.Column(db.Numeric)
    interestrate_initial=db.Column(db.Numeric)
    interestrate_floor=db.Column(db.Numeric)
    interestrate_protection=db.Column(db.Numeric)
    date_funding=db.Column(db.DateTime)
    date_maturityinitial=db.Column(db.DateTime)
    date_maturityExt_1=db.Column(db.DateTime)
    date_maturityExt_2=db.Column(db.DateTime)
    funding_total=db.Column(db.Numeric)
    funding_share=db.Column(db.Numeric)
    funding_initial=db.Column(db.Numeric)
    funding_future=db.Column(db.Numeric)
    fee_origination=db.Column(db.Numeric)
    fee_upfront=db.Column(db.Numeric)
    last_modified=db.Column(db.DateTime)


class LoanAbstractSchema(ma.Schema):
    class Meta:
        fields=('id','property','lender','loantype', 'ratetype','index','indexrate','indexspread','interestrate_initial', 'interestrate_floor','interestrate_protection',
                'date_funding','date_maturityinitial','date_maturityExt_1','date_maturityExt_2','funding_total','funding_share','funding_initial','funding_future',
                'fee_origination','fee_upfront','last_modified')

@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    return user if user else None



