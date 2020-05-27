from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

db = SQLAlchemy()

class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentId =  db.Column(db.Integer, nullable=False)
    stream = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def toDict(self):
        return{
            'id': self.id,
            'studentId': self.studentId,
            'stream': self.stream,
            'created': self.created.strftime("%m/%d/%Y, %H:%M:%S")
        }

class User(db.Model, UserMixin):
    id = db.Column(db.integer, primary_key=True)
    username = db.Column(db.string, nullable=False)
    email = db.Column(db.string, nullable=False)
    password = db.Column(db.string, nullable=False)

    def toDict(self):
        return{
            "ID ": self.id,
            "Username ": self.username,
            "Email ": self.email,
            "Password ": self.password
        }

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)
