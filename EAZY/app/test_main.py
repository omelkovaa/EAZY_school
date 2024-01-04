import unittest
from flask import Flask
from flask_testing import TestCase
from .__init__ import create_app, db
from .models import User, Course
from .config import *


class TestMainBlueprint(TestCase):

    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_US}:{DB_PA}@localhost:5432/postgres'
        return app

    def setUp(self):
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.create_all()
        test_user = User.query.filter_by(email='test@example.com').first()
        if test_user:
            db.session.delete(test_user)
            db.session.commit()

    def login(self):
        user = User(username='test', email='test@example.com', password='test_password', native_language='EN')
        db.session.add(user)
        db.session.commit()
        response = self.client.post('/login', data={'emailField': 'test@example.com', 'passwordField': 'test_password'})
        self.assertRedirects(response, '/about')

    def test_courses_resource(self):
        course = Course(name='Sample Course', description='Sample Description', duration=12, difficulty_level="a1-a1", language='EN')
        db.session.add(course)
        db.session.commit()

        response = self.client.get('/api/courses')
        self.assert200(response)
        self.assertEqual(response.json, [{'id': 34, 'name': 'Sample Course', 'description': 'Sample Description', 'duration': 12, 'difficulty_level': "a1-a1", 'language': 'EN'}])

    def test_index_route(self):
        response = self.client.get('/')
        self.assert200(response)

    def test_about_route(self):
        response = self.client.get('/about')
        self.assert200(response)

    def test_courses_route(self):
        response = self.client.get('/courses')
        self.assert200(response)


if __name__ == '__main__':
    unittest.main()
