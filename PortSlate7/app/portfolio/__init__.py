from flask import Blueprint

blueprint = Blueprint(
    'portfolio_blueprint',
    __name__,
    url_prefix='/portfolio',
    template_folder='templates',
    static_folder='static'
)
