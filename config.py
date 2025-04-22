import os

SECRET_KEY = 'alura'

SQLALCHEMY_DATABASE_URI = \
    '{SGDB}://{user}:{password}@{host}:{port}/{database}'.format(
        SGDB = 'mysql+pymysql',
        user = 'root',
        password = '',
        host = 'localhost',
        port = '3306',
        database = 'jogoteca'
    )
    
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/static/uploads'