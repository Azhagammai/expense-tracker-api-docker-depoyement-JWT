from flask import current_app
from flask_pymongo import PyMongo
from bson import ObjectId
from bson.errors import InvalidId

class DatabaseService:
    def __init__(self):
        self.mongo = None
    
    def init_app(self, app):
        self.mongo = PyMongo(app)
    
    def get_db(self):
        return self.mongo.db
    
    def get_collection(self, collection_name):
        return self.get_db()[collection_name]
    
    def insert_one(self, collection_name, document):
        """Insert a single document"""
        collection = self.get_collection(collection_name)
        result = collection.insert_one(document)
        return result.inserted_id
    
    def find_one(self, collection_name, query):
        """Find a single document"""
        collection = self.get_collection(collection_name)
        return collection.find_one(query)
    
    def find_many(self, collection_name, query=None, sort=None, limit=None):
        """Find multiple documents"""
        collection = self.get_collection(collection_name)
        cursor = collection.find(query or {})
        
        if sort:
            cursor = cursor.sort(sort)
        if limit:
            cursor = cursor.limit(limit)
            
        return list(cursor)
    
    def update_one(self, collection_name, query, update_data):
        """Update a single document"""
        collection = self.get_collection(collection_name)
        result = collection.update_one(query, {'$set': update_data})
        return result.modified_count > 0
    
    def delete_one(self, collection_name, query):
        """Delete a single document"""
        collection = self.get_collection(collection_name)
        result = collection.delete_one(query)
        return result.deleted_count > 0
    
    def delete_many(self, collection_name, query):
        """Delete multiple documents"""
        collection = self.get_collection(collection_name)
        result = collection.delete_many(query)
        return result.deleted_count
    
    def count_documents(self, collection_name, query=None):
        """Count documents matching query"""
        collection = self.get_collection(collection_name)
        return collection.count_documents(query or {})
    
    @staticmethod
    def is_valid_object_id(object_id):
        """Check if string is a valid ObjectId"""
        try:
            ObjectId(object_id)
            return True
        except (InvalidId, TypeError):
            return False

# Global database service instance
db_service = DatabaseService()
