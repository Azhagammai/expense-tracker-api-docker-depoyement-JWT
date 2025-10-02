from bson import ObjectId
from flask_bcrypt import generate_password_hash, check_password_hash
from marshmallow import Schema, fields, validate, ValidationError
import re

class User:
    def __init__(self, first_name, last_name, email, password, _id=None):
        self._id = _id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email.lower()
        self.password = password
    
    def to_dict(self):
        return {
            '_id': str(self._id) if self._id else None,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }
    
    def hash_password(self):
        """Hash the user's password"""
        self.password = generate_password_hash(self.password).decode('utf-8')
    
    @staticmethod
    def check_password(hashed_password, password):
        """Check if provided password matches the hashed password"""
        return check_password_hash(hashed_password, password)
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

class UserRegistrationSchema(Schema):
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6, max=100))

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=1))

# Sample user data for registration
sample_user_data = {
  "first_name": "azhagammai",
  "last_name": "yourlastname",
  "email": "your@email.com",
  "password": "yourpassword"
}
