from flask import jsonify
from marshmallow import ValidationError
from flask_jwt_extended.exceptions import JWTExtendedException
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    """Register global error handlers for the Flask app"""
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        """Handle Marshmallow validation errors"""
        return jsonify({
            'status': 'error',
            'message': 'Validation failed',
            'errors': e.messages
        }), 400
    
    @app.errorhandler(JWTExtendedException)
    def handle_jwt_exceptions(e):
        """Handle JWT related errors"""
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 401
    
    @app.errorhandler(ValueError)
    def handle_value_error(e):
        """Handle ValueError exceptions"""
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400
    
    @app.errorhandler(404)
    def handle_not_found(e):
        """Handle 404 errors"""
        return jsonify({
            'status': 'error',
            'message': 'Resource not found'
        }), 404
    
    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        """Handle method not allowed errors"""
        return jsonify({
            'status': 'error',
            'message': 'Method not allowed'
        }), 405
    
    @app.errorhandler(500)
    def handle_internal_error(e):
        """Handle internal server errors"""
        return jsonify({
            'status': 'error',
            'message': 'An internal server error occurred'
        }), 500
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """Handle other HTTP exceptions"""
        return jsonify({
            'status': 'error',
            'message': e.description
        }), e.code
