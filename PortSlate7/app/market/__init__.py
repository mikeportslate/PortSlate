from flask import Blueprint

blueprint = Blueprint(
    'market_blueprint',
    __name__,
    url_prefix='/market',
    template_folder='templates',
    static_folder='static'
)
