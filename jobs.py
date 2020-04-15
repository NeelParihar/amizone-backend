from apscheduler.schedulers.blocking import BlockingScheduler
from scraper.scraper import amizonebot
from models.user import UserModel
from models.attendance import AttendanceModel
from models.schedule import ScheduleModel
from app import app
import hashlib

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=1)
def timed_job():
    with app.app_context():
        users = UserModel.query.all()
        AttendanceModel.query.delete()
        ScheduleModel.query.delete()
        amizone = amizonebot()
        for user in users:
            
            amizone.login(user.username, user.password)
            schedule = amizone.getSchedule()
            attend = amizone.getAttendance()
            i = 1
            while i < len(attend):
                AttendanceModel(
                    user_id=user.id, course_name=attend[i-1], percentage=attend[i+1-1], ratio=attend[i+2-1]).save_to_db()
                i = i+3
            i = 1
            while i < len(schedule):
                ScheduleModel(
                    user_id=user.id, course_details=schedule[i], prof_name=schedule[i+1]).save_to_db()
                i = i+2


sched.start()
