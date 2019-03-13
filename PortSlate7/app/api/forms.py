# app/admin/forms.py

from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField


class LoanAbstractForm(FlaskForm):
    """
    Form for admin to add or edit a music record
    """
    property = wtforms.StringField('Property', validators=[DataRequired()])
    lender = wtforms.StringField('Lender', validators=[DataRequired()])
    loantype = wtforms.StringField('LoanType', validators=[DataRequired()])
    ratetype = wtforms.StringField('RateType', validators=[DataRequired()])
    index = wtforms.StringField('Index', validators=[DataRequired()])
    indexrate = wtforms.DecimalField('IndexRate')
    indexspread = wtforms.DecimalField('IndexSpread')
    interestrate_initial = wtforms.DecimalField('Initial Interest Rate')
    date_funding = wtforms.DateField('Date_Funding')
    date_maturityinitial = wtforms.DateField('Date_MaturityInitial')
    funding_total = wtforms.StringField('Funding_Total')



