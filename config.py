import os
import config_keys
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = config_keys.SECRET_KEY
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False