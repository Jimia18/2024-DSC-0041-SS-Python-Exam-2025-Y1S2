from flask import Blueprint,request,jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK
import validators
from app.models.program_model import Program
from app.extensions import db,bcrypt
from flask_jwt_extended import create_access_token,create_refresh_token
#program blueprint
program_bp = Blueprint('program', __name__,url_prefix='/api/v1/program')


# Create a new program
@program_bp.route('/create', methods=['POST'])
def create_program():
    
#storing request vaues
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    # Validate input
    if not name or not description:
        return jsonify({"error": "Name and description are required"}), HTTP_400_BAD_REQUEST

    # Check if program already exists
    existing_program = program.query.filter_by(name=name).first()
    if existing_program:
        return jsonify({"error": "Program already exists"}), HTTP_409_CONFLICT

    # Create new program
    new_program = program(name=name, description=description)
    db.session.add(new_program)
    db.session.commit()

    return jsonify({"message": "Program created successfully", "program_id": new_program.id}), HTTP_201_CREATED
def create_program():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    # Validate input
    if not name or not description:
        return jsonify({"error": "Name and description are required"}), HTTP_400_BAD_REQUEST

    # Check if program already exists
    existing_program = program.query.filter_by(name=name).first()
    if existing_program:
        return jsonify({"error": "Program already exists"}), HTTP_409_CONFLICT

    # Create new program
    new_program = program(name=name, description=description)
    db.session.add(new_program)
    db.session.commit()

    return jsonify({"message": "Program created successfully", "program_id": new_program.id}), HTTP_201_CREATED

# program login
@program_bp.route('/login',methods = ['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Validations
    if not password or not email:
        return jsonify({"error": "Email and password are required"}), HTTP_400_BAD_REQUEST
    program = program.User.query.filter_by(email=email).first()

    if program:
        is_correct_password = bcrypt.check_password_hash(program.password,password)
    

        if is_correct_password:
            access_token = create_access_token(identity={"program_id": program.id})
            refresh_token = create_refresh_token(identity={"program_id": program.id})
            return jsonify({
                'program':{
                    'id':program.id,
                    'name':program.name,
                    'email':program.email,
                    'description':program.description,
                    'access_token': access_token,
                    'refresh_token': refresh_token
                },
                "Message":"You have successfully logged into your account"
            }),HTTP_200_OK
        else:
            return jsonify({"error": "Invalid password"}), HTTP_401_UNAUTHORIZED

   



   