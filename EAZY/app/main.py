from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from flask_restful import Resource, Api, reqparse
from flask import Flask
from . import db
from . import forms
from .models import User, Teacher, Course
from flask_login import current_user, login_required

main = Blueprint('main', __name__)
api = Api(main)


@main.route('/', methods=('GET', 'POST'))
def index():
    form = forms.UserSub()

    email = request.form.get('emailField')
    username = request.form.get('usernameField')
    return render_template('index.html', form=form)


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(id=1).first()
    print(user.course)

    return render_template('profile.html', username=current_user.username, email=current_user.email,
                           native_language=current_user.native_language, courses=user.course)


@main.route('/courses')
def courses():
    courses = Course.query.all()
    print(courses)
    return render_template('courses.html', courses=courses)


@main.route('/profile_teacher')
def profile_teacher():
    return render_template('profile_teacher.html')


@main.route("/add_course/<int:id>", methods=['GET', 'POST'])
@login_required
def add_(id):
    try:
        if request.method == "POST":
            if "cart" in session:
                session["cart"] += [id]
                user = User.query.filter_by(id=current_user.get_id()).first()
                course = Course.query.filter_by(id=id).first()
                if course:
                    user.course.append(course)
                    user.verified = True
                    db.session.commit()
                return redirect('/courses')
            else:
                session["cart"] = []
                return redirect('/courses')
    except Exception as e:
        print(e)
    finally:
        return redirect('/courses')


@main.route("/remove_course/<int:id>", methods=['GET', 'POST'])
@login_required
def remove_course(id):
    try:
        if "cart" in session:
            session["cart"].remove(id)
            user = User.query.filter_by(id=current_user.get_id()).first()
            course = Course.query.filter_by(id=id).first()
            if course:
                user.course.remove(course)
                db.session.commit()
    except Exception as e:
        print(e)
    finally:
        return redirect('/profile')


parser = reqparse.RequestParser()
parser.add_argument('course_id', type=int, help='Course ID')


class CoursesResource(Resource):
    def get(self):
        courses = Course.query.all()
        course_list = [{'id': course.id, 'name': course.name, 'description': course.description} for course in courses]
        return jsonify(course_list)


class UserResource(Resource):
    @login_required
    def get(self):
        return jsonify({
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'native_language': current_user.native_language,
        })


class AddCourseResource(Resource):
    @login_required
    def post(self):
        args = parser.parse_args()
        course_id = args['course_id']

        if course_id:
            session["cart"] = session.get("cart", []) + [course_id]
            user = User.query.get(current_user.id)
            course = Course.query.get(course_id)
            if course:
                user.course.append(course)
                user.verified = True
                db.session.commit()

            return {'message': 'Course added successfully'}, 201
        else:
            return {'message': 'Invalid course ID'}, 400


class RemoveCourseResource(Resource):
    @login_required
    def post(self):
        args = parser.parse_args()
        course_id = args['course_id']

        if course_id:
            session["cart"] = [c for c in session.get("cart", []) if c != course_id]
            user = User.query.get(current_user.id)
            course = Course.query.get(course_id)
            if course:
                user.course.remove(course)
                db.session.commit()

            return {'message': 'Course removed successfully'}, 200
        else:
            return {'message': 'Invalid course ID'}, 400


class UserCartResource(Resource):
    @login_required
    def get(self):
        return jsonify(session.get("cart", []))


api.add_resource(CoursesResource, '/api/courses')
api.add_resource(UserResource, '/api/user')
api.add_resource(AddCourseResource, '/api/add_course/<int:id>')
api.add_resource(RemoveCourseResource, '/api/remove_course/<int:id>')
api.add_resource(UserCartResource, '/api/user_cart')

# /api/courses: список курсов
# /api/user: поулчение данных юзера
# /api/add_course: добавление курса юзеру
# /api/remove_course: удаление курсов юзера
# /api/user_cart: получение курсов юзера