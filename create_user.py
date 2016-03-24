#!/usr/bin/env python
"""Create a new admin user able to view the /reports endpoint."""
from getpass import getpass
import sys

from flask import current_app
from flaskserversocket import app, db,bcrypt
from models.models import User
#from flask.ext.bcrypt import Bcrypt

def main():
    """Main entry point for script."""
    with app.app_context():
        db.metadata.create_all(db.engine)
        if User.query.all():
            print 'A user already exists! Create another? (y/n):',
            create = raw_input()
            if create == 'n':
                return

        print 'Enter username address: ',
        username = raw_input()
        password = getpass()
        assert password == getpass('Password (again):')

        user = User(username=username, passw=bcrypt.generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        print 'User added.'



if __name__ == '__main__':
    sys.exit(main())