from app.extensions import db, migrate
from datetime import datetime

class Course(db.Model):
    __tablename__ = 'courses'
    course_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    courses = db.relationship('Course', backref='program', lazy=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    
    def __init__(self, name, description):
        self.name = name
        self.description = description  


        
    def __str__(self):
        return f"Course {self.name} with description {self.description}"
    