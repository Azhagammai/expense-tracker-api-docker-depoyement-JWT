from bson import ObjectId
from marshmallow import Schema, fields, validate
from config import Config

class Category:
    def __init__(self, title, description, user_id, _id=None):
        self._id = _id
        self.title = title
        self.description = description
        self.user_id = ObjectId(user_id) if isinstance(user_id, str) else user_id
    
    def to_dict(self):
        return {
            '_id': str(self._id) if self._id else None,
            'title': self.title,
            'description': self.description,
            'user_id': str(self.user_id)
        }
    
    @staticmethod
    def is_valid_category(title):
        """Check if the category title is in the predefined list"""
        return title in Config.EXPENSE_CATEGORIES

class CategorySchema(Schema):
    title = fields.Str(required=True, validate=validate.OneOf(Config.EXPENSE_CATEGORIES))
    description = fields.Str(required=True, validate=validate.Length(min=1, max=200))
