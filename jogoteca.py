from flask import Flask
from models import db
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

from views import *

if __name__ == '__main__':
    app.run(debug=True)