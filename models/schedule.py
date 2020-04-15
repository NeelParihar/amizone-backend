from database.db import db


class ScheduleModel(db.Model):
    __tablename__ = "schedule"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False,
    )
    course_details = db.Column(db.String())
    prof_name = db.Column(db.String())

    def __init__(self, user_id, course_details, prof_name):
        self.user_id = user_id
        self.course_details = course_details
        self.prof_name = prof_name

    def json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "course_details": self.course_details,
            "prof_name": self.prof_name
        }, 200

    # Method to save user to DB
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Method to remove user from DB
    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # Class method which finds course from DB by userid
    @classmethod
    def find_course_by_userid(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def deleteall(cls):
        records = cls.query.all()
        db.session.delete(records)
        db.session.commit()

