from flask_migrate import Migrate
import os
from os import environ
from sys import exit

from config import config_dict
from app import create_app, db

get_config_mode = environ.get('PORTSLATE_CONFIG_MODE', 'Production')
config_mode = config_dict[get_config_mode.capitalize()]

application = create_app(config_mode)
Migrate(application, db)
# os.remove('error.log')


if __name__ == '__main__':
    application.run()