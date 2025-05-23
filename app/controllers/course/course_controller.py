from flask import Blueprint,request,jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_201_CREATED 
import validators
from app.models.course_model import Course
from app.extensions import db,bcrypt
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity

#course blueprint
course_bp = Blueprint('course', __name__,url_prefix='/api/v1/course')
# Create a new course
@course_bp.route('/create', methods=['POST'])
def create_course():

    #storing request vaues
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    # Validate input
    if not name or not description:
        return jsonify({"error": "Name and description are required"}), HTTP_400_BAD_REQUEST

    # Check if course already exists
    existing_course = Course.query.filter_by(name=name).first()
    if existing_course:
        return jsonify({"error": "Course already exists"}), HTTP_409_CONFLICT

    # Create new course
    new_course = Course(name=name, description=description)
    db.session.add(new_course)
    db.session.commit()

    return jsonify({"message": "Course created successfully", "course_id": new_course.id}), HTTP_201_CREATED
    