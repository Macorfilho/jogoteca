

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