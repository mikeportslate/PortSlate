from flask import Blueprint

blueprint = Blueprint(
    'investors_blueprint',
    __name__,
    url_prefix='/investors',
    static_folder='static'
)
