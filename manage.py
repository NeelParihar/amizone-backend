from flask_script import Manager

import app, models
from database.db import db
from models import UserModel


import os

from random import randint
from sqlalchemy.exc import IntegrityError

# Initializing the manager
manager = Manager(app)

# Initialize Flask Migrate
migrate = Migrate(app, db)

# Add the flask migrate
manager.add_command('db', MigrateCommand)



# Add test command
@manager.command
def test():
    """
    Run tests without coverage
    :return:
    """
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def dummy():
    # Create a user if they do not exist.
    user = UserModel.find_user_by_username(username="example@bucketmail.com").first()
    if not user:
        user = UserModel("example@bucketmail.com", "123456")
        user.save()
        


# Run the manager
if __name__ == '__main__':
    manager.run()