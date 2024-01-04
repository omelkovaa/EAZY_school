from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .config import *

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_US}:{DB_PA}@localhost:5432/postgres'
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    babel = Babel(app)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import Teacher, Course, User, enrollment

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    admin = Admin(app, name='ADMIN', template_mode='bootstrap3')
    admin.add_view(ModelView(Teacher, db.session, name='Teacher'))
    admin.add_view(ModelView(Course, db.session, name='Course'))
    admin.add_view(ModelView(User, db.session, name='User'))

    return app