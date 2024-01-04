from flask_login import UserMixin
from . import db


enrollment = db.Table('enrollment', db.Column('users', db.Integer, db.ForeignKey('users.id')),
                      db.Column('courses', db.Integer, db.ForeignKey('courses.id')))




class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    native_language = db.Column(db.String(50), nullable=False)
    course = db.relationship('Course', secondary=enrollment, back_populates='user')

    def __repr__(self):
        return f'{self.email}-{self.username}'

class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    biography = db.Column(db.Text, nullable=False)
    specialization = db.Column(db.String(255), nullable=False)
    availability_schedule = db.Column(db.Text, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    difficulty_level = db.Column(db.String(50), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    user = db.relationship('User', secondary=enrollment, back_populates='course')






