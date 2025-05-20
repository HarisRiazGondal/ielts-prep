import os
import uuid
import mimetypes
import logging
from werkzeug.utils import secure_filename
from flask import current_app

# Setup module logger
logger = logging.getLogger(__name__)

# Try to import magic for better MIME detection, use fallback if not available
MAGIC_AVAILABLE = False
try:
    import magic
    MAGIC_AVAILABLE = True
except (ImportError, OSError):
    logger.warning("python-magic or libmagic not available, using mimetypes fallback for MIME type detection")

class FileUploader:
    """Utility for handling file uploads securely"""
    
    @staticmethod
    def allowed_file(filename, file_type=None):
        """Check if a filename has an allowed extension"""
        if '.' not in filename:
            return False
            
        if not file_type:
            # Check against all allowed extensions
            allowed_extensions = []
            for extensions in current_app.config['ALLOWED_EXTENSIONS'].values():
                allowed_extensions.extend(extensions)
        else:
            if file_type not in current_app.config['ALLOWED_EXTENSIONS']:
                return False
            allowed_extensions = current_app.config['ALLOWED_EXTENSIONS'][file_type]
        
        ext = filename.rsplit('.', 1)[1].lower()
        return ext in allowed_extensions
    
    @staticmethod
    def get_mime_type(filepath):
        """Get MIME type using magic if available, fallback to mimetypes"""
        if MAGIC_AVAILABLE:
            try:
                mime = magic.Magic(mime=True)
                return mime.from_file(filepath)
            except Exception as e:
                logger.error(f"Error with magic MIME detection: {str(e)}")
        
        # Fallback to mimetypes
        mime_type, _ = mimetypes.guess_type(filepath)
        return mime_type or 'application/octet-stream'
    
    @staticmethod
    def save_file(file, directory, file_type=None, check_content=True):
        """
        Save a file securely
        
        Args:
            file: The file object from request.files
            directory: Directory within UPLOAD_FOLDER to save to
            file_type: Type of file ('image', 'audio', etc.) for validation
            check_content: Whether to verify MIME type
        
        Returns:
            Tuple of (success, filename or error message)
        """
        if not file or file.filename == '':
            return (False, 'No file selected')
            
        if not FileUploader.allowed_file(file.filename, file_type):
            return (False, 'File type not allowed')
            
        # Create a secure filename with a UUID to prevent collisions
        original_name = secure_filename(file.filename)
        name, ext = original_name.rsplit('.', 1)
        unique_filename = f"{name}_{uuid.uuid4().hex[:8]}.{ext}"
        
        # Ensure the target directory exists
        target_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], directory)
        os.makedirs(target_dir, exist_ok=True)
        
        # Full path to save the file
        filepath = os.path.join(target_dir, unique_filename)
        
        try:
            # Save the file temporarily to check content type
            file.save(filepath)
            
            # Optionally verify the MIME type
            if check_content:
                content_type = FileUploader.get_mime_type(filepath)
                
                # Map acceptable MIME types by file category
                mime_map = {
                    'image': ['image/jpeg', 'image/png', 'image/gif', 'image/svg+xml', 'image/webp'],
                    'audio': ['audio/mpeg', 'audio/mp4', 'audio/ogg', 'audio/wav', 'audio/webm'],
                    'document': ['application/pdf', 'application/msword', 
                                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                                'text/plain']
                }
                
                if file_type and file_type in mime_map:
                    if content_type not in mime_map[file_type]:
                        # Content doesn't match claimed type - delete and return error
                        os.unlink(filepath)
                        return (False, f"File content doesn't match {file_type} type")
            
            # Return the path relative to the upload folder
            relative_path = os.path.join(directory, unique_filename)
            return (True, relative_path)
            
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            # Clean up if the file was saved
            if os.path.exists(filepath):
                try:
                    os.unlink(filepath)
                except:
                    pass
            return (False, f"Error saving file: {str(e)}")

    @staticmethod
    def delete_file(filename):
        """Delete a file from the uploads directory"""
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        try:
            if os.path.exists(filepath):
                os.unlink(filepath)
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file {filepath}: {str(e)}")
            return False 