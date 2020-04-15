from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, fresh_jwt_required
from flask import jsonify
from models.user import UserModel
from models.attendance import AttendanceModel
from models.schedule import ScheduleModel
from scraper.scraper import amizonebot
import datetime
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


class Index(Resource):
    def get(self):
        return {
            "message": "Hello world!"
        }, 200


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


class GetCurrentUser(Resource):
    @fresh_jwt_required
    def get(self):
        user = UserModel.find_user_by_id(get_jwt_identity())
        if user:
            return user.json()

        return {
            "message": "User not found!"
        }, 404


class UserLogin(Resource):
    def post(self):
        data = _user_parser.parse_args()

        user = UserModel.find_user_by_username(data["username"])
        expires = datetime.timedelta(days=30)
        if user and user.password == hashlib.sha256(data["password"].encode("utf-8")).hexdigest():
            # Puts User ID as Identity in JWT
            access_token = create_access_token(
                identity=user.id, fresh=True, expires_delta=expires)
            refresh_token = create_refresh_token(
                identity=user.id)  # Puts User ID as Identity in JWT
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200

        amizone = amizonebot()
        scraperdata = amizone.login(
            usern=data["username"], passw=data["password"])

        user = UserModel(data["username"], hashlib.sha256(data["password"].encode(
            "utf-8")).hexdigest(), scraperdata["fullname"], scraperdata["profilepic"])
        user.save_to_db()
        i = 0
        attend = amizone.getAttendance()
        while i < len(attend):
            AttendanceModel(
                user_id=user.id, course_name=attend[i], percentage=attend[i+1], ratio=attend[i+2]).save_to_db()
            i = i+3

        schedule = amizone.getSchedule()
        i = 1
        while i < len(schedule):
            ScheduleModel(
                user_id=user.id, course_details=schedule[i], prof_name=schedule[i+1]).save_to_db()
            i = i+2

        # except:
        #     print(Exception.__name__)
        #     return {
        #         "message": "User not found!"
        #     }, 404
        # finally:
        #     return {
        #         "message": "User not found!"
        #     }, 404

            # Puts User ID as Identity in JWT
        access_token = create_access_token(
            identity=user.id, fresh=True, expires_delta=expires)
        refresh_token = create_refresh_token(identity=user.id)

        return {
            "message": "User {} created!".format(data["username"]),
            "access_token": access_token,
            "refresh_token": refresh_token
        }, 200


class GetAttendance(Resource):
    @fresh_jwt_required
    def get(self):
        attend = AttendanceModel.find_course_by_userid(get_jwt_identity())
        if attend:
            all_attend = [{'CourseName': user.course_name,
                           'Percentage': user.percentage, 'Ratio': user.ratio} for user in attend]
            return jsonify(all_attend)

        return {
            "message": "User not found!"
        }, 404


class GetSchedule(Resource):
    @fresh_jwt_required
    def get(self):
        schedule = ScheduleModel.find_course_by_userid(get_jwt_identity())
        if schedule:
            all_rows = [{'CourseDetails': user.course_details,
                         'ProfDeatils': user.prof_name} for user in schedule]
            return jsonify(all_rows)

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
