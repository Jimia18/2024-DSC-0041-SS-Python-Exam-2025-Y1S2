from app.extensions import db, migrate
from datetime import datetime

class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.program_id'), nullable=False)
    courses = db.relationship('Course', secondary='enrollments', backref='students', lazy=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)        

   

def __str__(self):
        return f"Student {self.name} with email {self.email}"
def __init__(self, name, email, program_id):
        self.name = name
        self.email = email
        self.program_id = program_id