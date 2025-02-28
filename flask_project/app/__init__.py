from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_restx import Api

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# api = Api(app, doc='/api', title='Task Management API', description='Task Management API with Flask-RESTX and JWT')
api = Api(app, 
          title='Task Management API', 
          description='API for managing tasks', 
          default_mediatype='application/json',
          mask_swagger=False)

from app import routes, models