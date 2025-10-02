from bson import ObjectId
from models.user import User
from services.database import db_service
from flask_jwt_extended import create_access_token

class UserService:
    @staticmethod
    def create_user(first_name, last_name, email, password):
        """Create a new user"""
        # Check if user already exists
        existing_user = db_service.find_one('users', {'email': email.lower()})
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Create new user
        user = User(first_name, last_name, email, password)
        user.hash_password()
        
        # Insert into database
        user_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'password': user.password
        }
        
        user_id = db_service.insert_one('users', user_data)
        user._id = user_id
        
        return user
    
    @staticmethod
    def authenticate_user(email, password):
        """Authenticate user with email and password"""
        user_data = db_service.find_one('users', {'email': email.lower()})
        
        if not user_data:
            raise ValueError("Invalid email or password")
        
        if not User.check_password(user_data['password'], password):
            raise ValueError("Invalid email or password")
        
        user = User(
            user_data['first_name'],
            user_data['last_name'], 
            user_data['email'],
            user_data['password'],
            user_data['_id']
        )
        
        return user
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        if not db_service.is_valid_object_id(user_id):
            return None
            
        user_data = db_service.find_one('users', {'_id': ObjectId(user_id)})
        
        if not user_data:
            return None
        
        user = User(
            user_data['first_name'],
            user_data['last_name'],
            user_data['email'],
            user_data['password'],
            user_data['_id']
        )
        
        return user
    
    @staticmethod
    def generate_token(user):
        """Generate JWT token for user"""
        identity = {
            'user_id': str(user._id),
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        
        return create_access_token(identity=identity)
