import os
import hashlib
from flask import current_app, url_for

class AssetManager:
    """Asset management utilities for the application"""
    
    _asset_hash_cache = {}
    
    @staticmethod
    def url_for(endpoint, **values):
        """Generate a URL with asset versioning if applicable"""
        if endpoint == 'static' and current_app.config.get('ASSET_VERSIONING'):
            filename = values.get('filename', '')
            if filename:
                values['v'] = AssetManager.get_asset_version(filename)
        
        if current_app.config.get('CDN_DOMAIN') and endpoint == 'static':
            # Use CDN for static assets
            filename = values.get('filename', '')
            cdn_url = current_app.config['CDN_DOMAIN'].rstrip('/')
            app_static_path = url_for('static', filename='', _external=False).rstrip('/')
            asset_url = f"{cdn_url}{app_static_path}/{filename}"
            
            # Add version parameter if enabled
            if current_app.config.get('ASSET_VERSIONING'):
                version = values.get('v', AssetManager.get_asset_version(filename))
                asset_url = f"{asset_url}?v={version}"
                
            return asset_url
        
        # Fall back to standard url_for
        return url_for(endpoint, **values)
    
    @staticmethod
    def get_asset_version(filename):
        """Get the version hash for an asset file"""
        # Use global asset version if specified
        if current_app.config.get('ASSET_VERSION'):
            return current_app.config['ASSET_VERSION']
        
        # Otherwise calculate file hash
        if filename in AssetManager._asset_hash_cache:
            return AssetManager._asset_hash_cache[filename]
        
        try:
            file_path = os.path.join(current_app.root_path, 'static', filename)
            if not os.path.exists(file_path):
                return '1'
                
            with open(file_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()[:8]
                AssetManager._asset_hash_cache[filename] = file_hash
                return file_hash
        except:
            # Return a default version on error
            return '1'
    
    @staticmethod
    def add_cache_headers(response):
        """Add appropriate cache headers to the response"""
        if not response.headers.get('Cache-Control'):
            if request.path.startswith('/static/'):
                # Cache static assets longer
                timeout = current_app.config.get('STATIC_CACHE_TIMEOUT', 86400)  # Default to 1 day
                response.headers['Cache-Control'] = f'public, max-age={timeout}'
            else:
                # Default cache control for dynamic content
                timeout = current_app.config.get('CACHE_DEFAULT_TIMEOUT', 300)  # Default to 5 minutes
                response.headers['Cache-Control'] = f'private, max-age={timeout}'
                
        return response
    
    @staticmethod
    def register_asset_helpers(app):
        """Register asset management helpers with the Flask application"""
        # Register asset_url template function
        @app.template_global()
        def asset_url_for(endpoint, **values):
            return AssetManager.url_for(endpoint, **values)
        
        # Add cache headers after each request
        @app.after_request
        def add_cache_headers(response):
            from flask import request
            
            if not response.headers.get('Cache-Control'):
                if request.path.startswith('/static/'):
                    # Cache static assets longer
                    timeout = app.config.get('STATIC_CACHE_TIMEOUT', 86400)  # Default to 1 day
                    response.headers['Cache-Control'] = f'public, max-age={timeout}'
                else:
                    # Default cache control for dynamic content
                    timeout = app.config.get('CACHE_DEFAULT_TIMEOUT', 300)  # Default to 5 minutes
                    response.headers['Cache-Control'] = f'private, max-age={timeout}'
                    
            return response 