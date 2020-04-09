from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import User, UserRegister, UserLogin , GetAttendance , GetSchedule

import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://neel:9870154473@127.0.0.1:5432/amizone"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = "v3ry_s3cr3t_k3y"
api = Api(app)

jwt = JWTManager(app)


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify(
        {
            "description": "Token has expired!",
            "error": "token_expired"
        }, 401
    )


@jwt.invalid_token_loader
def invalid_token_callback():
    return jsonify(
        {
            "description": "Signature verification failed!",
            "error": "invalid_token"
        }, 401
    )


@jwt.unauthorized_loader
def unauthorized_loader_callback(error):
    return jsonify(
        {
            "description": "Access token not found!",
            "error": "unauthorized_loader"
        }, 401
    )


@jwt.needs_fresh_token_loader
def fresh_token_loader_callback():
    return jsonify(
        {
            "description": "Token is not fresh. Fresh token needed!",
            "error": "needs_fresh_token"
        }, 401
    )


api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(GetAttendance,"/attendance/<int:user_id>")
api.add_resource(GetSchedule,"/schedule/<int:user_id>")

if __name__ == '__main__':
    from database.db import db

    db.init_app(app)


    @app.before_first_request
    def create_tables():
        db.create_all()


    app.run(port=5000, debug=True)