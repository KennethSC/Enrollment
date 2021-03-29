from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_restplus import Api

api = Api(doc='/apiv1', prefix="/apiv1")
app = Flask(__name__)
app.config.from_object(Config)

db = MongoEngine()
db.init_app(app)
api.init_app(app)

from application import routes, API