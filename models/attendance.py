from database.db import db


class AttendanceModel(db.Model):
    __tablename__ = "attendance"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )
    course_name = db.Column(db.String())
    percentage = db.Column(db.String())
    ratio = db.Column(db.String())

    def __init__(self, user_id, course_name, percentage, ratio):
        self.user_id = user_id
        self.course_name = course_name
        self.percentage = percentage
        self.ratio = ratio

    def json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "course_name": self.course_name,
            "percentage": self.percentage,
            "ratio": self.ratio
        }, 200

    # Method to save user to DB
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Method to remove user from DB
    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # Class method which finds user from DB by username
    @classmethod
    def find_course_by_userid(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    # Class method which finds user from DB by id
    @classmethod
    def find_user_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
