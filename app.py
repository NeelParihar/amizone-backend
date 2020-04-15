from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from database.db import db
from resources.user import User, UserLogin, GetAttendance, GetCurrentUser, GetSchedule, Index

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://jfncuipbmptfyv:12dfaa5d6c0689f687d44b7cfe7c7e35245ab955523b8146c4deed8796f322c1@ec2-3-234-109-123.compute-1.amazonaws.com:5432/df9d3di7k6kd86"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = "v3ry_s3cr3t_k3y"
api = Api(app)


db.init_app(app)
jwt = JWTManager(app)


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify(
        {
            "description": "Token has expired!",
            "error": "token_expired"
        }, 404
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


api.add_resource(Index, "/")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(GetCurrentUser, "/user")
api.add_resource(UserLogin, "/login")
api.add_resource(GetAttendance, "/attendance")
api.add_resource(GetSchedule, "/schedule")

if __name__ == '__main__':

    @app.before_first_request
    def create_tables():
        db.create_all()
    app.run()
