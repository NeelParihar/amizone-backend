from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, fresh_jwt_required
from flask import jsonify
from models.user import UserModel
from models.attendance import AttendanceModel
from scraper.scraper import amizonebot
import hashlib

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    "username",
    type=str,
    required=True,
    help="This field cannot be blank"
)
_user_parser.add_argument(
    "password",
    type=str,
    required=True,
    help="This field cannot be blank"
)


class User(Resource):
    def get(self, user_id):
        user = UserModel.find_user_by_id(user_id)
        if user:
            return user.json()

        return {
                   "message": "User not found!"
               }, 404

    @fresh_jwt_required
    def delete(self, user_id):
        user = UserModel.find_user_by_id(user_id)
        if user:
            user.remove_from_db()
            return {
                       "message": "User deleted!"
                   }, 200

        return {
                   "message": "User not found!"
               }, 404


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_user_by_username(data["username"]):
            return {
                       "message": "User exists!"
                   }, 400

        #user = UserModel(data["username"], hashlib.sha256(data["password"].encode("utf-8")).hexdigest())
        #user.save_to_db()
        return {
            "message": "User {} created!".format(data["username"])
        }


class UserLogin(Resource):
    def post(self):
        data = _user_parser.parse_args()

        user = UserModel.find_user_by_username(data["username"])

        if user and user.password == hashlib.sha256(data["password"].encode("utf-8")).hexdigest():
            access_token = create_access_token(identity=user.id, fresh=True)  # Puts User ID as Identity in JWT
            refresh_token = create_refresh_token(identity=user.id)  # Puts User ID as Identity in JWT
            return {
                       "access_token": access_token,
                       "refresh_token": refresh_token
                   }, 200
        amizone = amizonebot()
        scraperdata=amizone.login(usern=data["username"],passw=data["password"])
        attend = amizone.getAttendance()
        #amizone.getSchedule()
        user = UserModel(data["username"], hashlib.sha256(data["password"].encode("utf-8")).hexdigest(),scraperdata["fullname"],scraperdata["profilepic"])
        user.save_to_db()
        i=0
        while i < len(attend):
            AttendanceModel(user_id=user.id,course_name=attend[i],percentage=attend[i+1],ratio=attend[i+2]).save_to_db()
            i=i+3

        access_token = create_access_token(identity=user.id, fresh=True)  # Puts User ID as Identity in JWT
        refresh_token = create_refresh_token(identity=user.id)

        return {
            "message": "User {} created!".format(data["username"]),
            "access_token": access_token,
            "refresh_token": refresh_token
        },200

class GetAttendance(Resource):
    @fresh_jwt_required
    def get(self,user_id):
        attend = AttendanceModel.find_course_by_userid(user_id)
        if attend:
            all_attend = [{'CourseName':user.course_name,'Percentage':user.percentage,'Ratio':user.ratio} for user in attend]
            print(all_attend)
            return jsonify(all_attend)

        return {
                   "message": "User not found!"
               }, 404


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user_id = get_jwt_identity()  # Gets Identity from JWT
        new_token = create_access_token(identity=current_user_id, fresh=False)
        return {
                   "access_token": new_token
               }, 200 