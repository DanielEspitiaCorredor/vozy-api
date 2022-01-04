from datetime import timedelta
from os import environ

from flask import Flask
from flask_jwt_extended import JWTManager

# App configuration
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': environ['MONGO_DATABASE'],
    'host': environ['MONGO_DBHOST'],
    'port': int(environ['MONGO_PORT']),
    'username': environ['MONGO_USERNAME'],
    "password": environ['MONGO_PASS']
}

app.config["JWT_ISSUER"]     = environ['JWT_ISSUER']
app.config["JWT_ALGORITHM"]  = environ['JWT_ALGORITHM']
app.config["JWT_SECRET_KEY"] = environ['JWT_SECRET_KEY']
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=int(environ['JWT_ACCESS_TOKEN_EXPIRES']))

jwt = JWTManager(app)

# User app routes.
import vozy_api.users.auth
