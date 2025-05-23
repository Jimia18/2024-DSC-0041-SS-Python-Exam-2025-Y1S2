from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED, HTTP_200_OK
import validators
from app.models.student_model import Student
from app.extensions import db, bcrypt
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity


student_bp = Blueprint('student', __name__, url_prefix='/api/v1/student')
# Create a new student
@student_bp.route('/create', methods=['POST'])
def create_student():

    # Store request values
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # Validate input
    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password are required"}), HTTP_400_BAD_REQUEST

    # Check if student already exists
    existing_student = Student.query.filter_by(email=email).first()
    if existing_student:
        return jsonify({"error": "Student already exists"}), HTTP_409_CONFLICT

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create new student
    new_student = Student(name=name, email=email, password=hashed_password)
    db.session.add(new_student)
    db.session.commit()

    return jsonify({"message": "Student created successfully", "student_id": new_student.id}), HTTP_201_CREATED

# Get student details
@student_bp.route('/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student(student_id):
    current_user = get_jwt_identity()
    if current_user['student_id'] != student_id:
        return jsonify({"error": "Unauthorized access"}), HTTP_401_UNAUTHORIZED

    student = Student.query.get_or_404(student_id)
    return jsonify({
        "id": student.id,
        "name": student.name,
        "email": student.email
    }), HTTP_200_OK

# Delete student details
@student_bp.route('/<int:student_id>', methods=['DELETE'])
@jwt_required()
def delete_student(student_id):
    current_user = get_jwt_identity()
    if current_user['student_id'] != student_id:
        return jsonify({"error": "Unauthorized access"}), HTTP_401_UNAUTHORIZED

    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()

    return jsonify({"message": "Student deleted successfully"}), HTTP_200_OK
