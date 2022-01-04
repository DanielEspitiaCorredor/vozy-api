from app import app
from flask import request
from flask_jwt_extended import create_access_token
from vozy_api import errors
from vozy_api.decorators import validate_request
from vozy_api.transactions import DatabaseTransaction
from vozy_api.users.exceptions import RegisterError
from vozy_api.users.models import User
from werkzeug.security import check_password_hash, generate_password_hash

REGISTER_KEY_PARAMS = {
    "POST": ["username", "name", "password", "email"]
}
LOGIN_KEY_PARAMS = {
    "POST": ["username", "password"]
}

user_manager = DatabaseTransaction(model=User)

@app.route("/auth/register", methods=["POST"])
@validate_request(body_keys=REGISTER_KEY_PARAMS)
def register():
    try:
        
        body = request.get_json()
        password = generate_password_hash(body["password"], method="pbkdf2:sha256")
        
        
        # Validate if user exists in the DB
        user_saved = user_manager.read(
            email=body["email"],
            username=body["username"],
            options={
                "query_operator": "OR",
                "first": True,
            }
        )
        
        if user_saved:
            raise RegisterError("User registration error")
        
        body['password'] = password
        
        user_manager.create(
            **body
        )
                
        return(
            {
                "message": "User registered"
            }, 200
        )
    except RegisterError:
        return errors.ERR_REGISTER_ERROR
    except Exception as e:
        print(e)
        return errors.ERR_UNCONTROLLED_EXCEPTION


@app.route("/auth/login", methods=["POST"])
@validate_request(body_keys=LOGIN_KEY_PARAMS)
def login():
    """
    Endpoint used to log in users in Vozy API
    """
    try:
        body = request.get_json()
        user = user_manager.read(
            username=body["username"],
            options={
                "first": True
            }
        )
        
        print(user)
        if not user or not check_password_hash(user.password, body["password"]):
            return errors.ERR_AUTH
        
        return (
            {
                "id": str(user.id),
                "access_token": create_access_token(identity=str(user.id))
            }, 200
        )
    except Exception as e:
        print(e)
        return errors.ERR_UNCONTROLLED_EXCEPTION