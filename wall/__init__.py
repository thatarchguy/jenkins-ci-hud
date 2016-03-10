from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)

from wall.api import wall_api
app.config.from_object('config.BaseConfiguration')
app.register_blueprint(wall_api)


from wall import views, models
