import traceback
import logging
from flask import render_template, jsonify, request, current_app
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError, DatabaseError
from werkzeug.http import HTTP_STATUS_CODES

logger = logging.getLogger(__name__)

class ErrorResponse:
    """Standardized error response structure"""
    
    @staticmethod
    def make_error(status_code, message=None, error_type=None, details=None):
        """Create a standardized error response"""
        if not message:
            message = HTTP_STATUS_CODES.get(status_code, 'Unknown error')
        
        response = {
            "error": {
                "status": status_code,
                "message": message
            }
        }
        
        if error_type:
            response["error"]["type"] = error_type
        
        if details:
            response["error"]["details"] = details
            
        return response

def register_error_handlers(app):
    """Register error handlers with the Flask application"""
    
    @app.errorhandler(400)
    def bad_request_error(error):
        logger.warning(f"400 Bad Request: {request.path} - {error}")
        if request.is_json:
            return jsonify(ErrorResponse.make_error(400)), 400
        return render_template('errors/400.html', error=error), 400

    @app.errorhandler(401)
    def unauthorized_error(error):
        logger.warning(f"401 Unauthorized: {request.path} - {error}")
        if request.is_json:
            return jsonify(ErrorResponse.make_error(401)), 401
        return render_template('errors/401.html', error=error), 401
    
    @app.errorhandler(403)
    def forbidden_error(error):
        logger.warning(f"403 Forbidden: {request.path} - {error}")
        if request.is_json:
            return jsonify(ErrorResponse.make_error(403)), 403
        return render_template('errors/403.html', error=error), 403

    @app.errorhandler(404)
    def not_found_error(error):
        logger.info(f"404 Not Found: {request.path}")
        if request.is_json:
            return jsonify(ErrorResponse.make_error(404)), 404
        return render_template('errors/404.html', error=error), 404
    
    @app.errorhandler(405)
    def method_not_allowed_error(error):
        logger.warning(f"405 Method Not Allowed: {request.method} {request.path}")
        if request.is_json:
            return jsonify(ErrorResponse.make_error(405)), 405
        return render_template('errors/405.html', error=error), 405

    @app.errorhandler(429)
    def too_many_requests_error(error):
        logger.warning(f"429 Too Many Requests: {request.path}")
        if request.is_json:
            return jsonify(ErrorResponse.make_error(429)), 429
        return render_template('errors/429.html', error=error), 429

    @app.errorhandler(500)
    def internal_server_error(error):
        logger.error(f"500 Internal Server Error: {request.path}\n{traceback.format_exc()}")
        if request.is_json:
            return jsonify(ErrorResponse.make_error(500)), 500
        return render_template('errors/500.html', error=error), 500

    @app.errorhandler(SQLAlchemyError)
    def handle_db_error(error):
        logger.error(f"Database Error: {str(error)}\n{traceback.format_exc()}")
        if request.is_json:
            return jsonify(ErrorResponse.make_error(
                500, 
                message="Database operation failed", 
                error_type="database_error",
                details=str(error) if app.debug else None
            )), 500
        return render_template('errors/500.html', 
                              error="A database error occurred. Please try again later."), 500

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        # Catch-all for unhandled exceptions
        logger.error(f"Unhandled Exception: {str(error)}\n{traceback.format_exc()}")
        if request.is_json:
            return jsonify(ErrorResponse.make_error(
                500, 
                message="An unexpected error occurred", 
                error_type="server_error",
                details=str(error) if app.debug else None
            )), 500
        return render_template('errors/500.html', error=error), 500 