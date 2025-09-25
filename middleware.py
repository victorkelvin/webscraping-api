"""
Security middleware and rate limiting for the API
"""

from functools import wraps
from flask import request, jsonify, g
from urllib.parse import urlparse
import time
from collections import defaultdict, deque
import hashlib
import logging
import os

logger = logging.getLogger(__name__)

class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self):
        self.requests = defaultdict(deque)
        self.blocked_ips = {}
    
    def is_allowed(self, identifier, limit=100, window=3600):
        """
        Checks if a request is allowed
        Args:
            identifier: IP or unique identifier
            limit: Maximum number of requests
            window: Time window in seconds
        """
        now = time.time()
        
        # Check if IP is temporarily blocked
        if identifier in self.blocked_ips:
            if now < self.blocked_ips[identifier]:
                return False
            else:
                del self.blocked_ips[identifier]
        
        # Clean up old requests
        while (self.requests[identifier] and 
               now - self.requests[identifier][0] > window):
            self.requests[identifier].popleft()
        
        # Check limit
        if len(self.requests[identifier]) >= limit:
            # Block for 1 hour
            self.blocked_ips[identifier] = now + 3600
            logger.warning(f"Rate limit exceeded for {identifier}")
            return False
        
        # Add current request
        self.requests[identifier].append(now)
        return True

class SecurityMiddleware:
    """Security middleware"""
    
    def __init__(self, app=None):
        self.app = app
        self.rate_limiter = RateLimiter()
        
        # Suspicious domains (example)
        self.suspicious_domains = {
            'malware.com', 'phishing.net', 'spam.org'
        }
        
        # Suspicious patterns in URLs
        self.suspicious_patterns = [
            'admin', 'login', 'password', 'secret', 'private'
        ]
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initializes the middleware with the Flask app"""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
    
    def before_request(self):
        """Runs before each request"""
        # Rate limiting
        client_ip = self.get_client_ip()
        
        if not self.rate_limiter.is_allowed(client_ip):
            return jsonify({
                'error': 'Rate limit exceeded',
                'message': 'Too many requests. Please try again later.',
                'status': 'error'
            }), 429
        
        # Security validation for scraping URLs
        if request.endpoint in ['scrape_page', 'scrape_products']:
            data = request.get_json()
            if data and 'url' in data:
                if not self.is_safe_url(data['url']):
                    return jsonify({
                        'error': 'URL not allowed',
                        'message': 'This URL is not permitted for scraping',
                        'status': 'error'
                    }), 403
        
        # Request log
        g.request_start_time = time.time()
        logger.info(f"Request: {request.method} {request.path} from {client_ip}")
    
    def after_request(self, response):
        """Runs after each request"""
        # Security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Log response time
        if hasattr(g, 'request_start_time'):
            duration = time.time() - g.request_start_time
            logger.info(f"Response: {response.status_code} in {duration:.3f}s")
        
        return response
    
    def get_client_ip(self):
        """Gets the real client IP"""
        # Check proxy headers
        if request.headers.get('X-Forwarded-For'):
            return request.headers.get('X-Forwarded-For').split(',')[0].strip()
        elif request.headers.get('X-Real-IP'):
            return request.headers.get('X-Real-IP')
        else:
            return request.remote_addr
    
    def is_safe_url(self, url):
        """Checks if a URL is safe for scraping"""
        try:
            parsed = urlparse(url.lower())
            domain = parsed.netloc
            
            # Check suspicious domains
            if domain in self.suspicious_domains:
                logger.warning(f"Blocked suspicious domain: {domain}")
                return False
            
            # Check suspicious patterns in path
            path = parsed.path.lower()
            for pattern in self.suspicious_patterns:
                if pattern in path:
                    logger.warning(f"Blocked suspicious pattern '{pattern}' in URL: {url}")
                    return False
            
            # Check allowed schemes
            if parsed.scheme not in ['http', 'https']:
                logger.warning(f"Blocked non-HTTP scheme: {parsed.scheme}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating URL {url}: {e}")
            return False

def require_json(f):
    """Decorator that requires Content-Type application/json"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type must be application/json',
                'status': 'error'
            }), 400
        return f(*args, **kwargs)
    return decorated_function

def validate_url_param(f):
    """Decorator that validates the URL parameter"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                'error': 'URL parameter is required',
                'status': 'error'
            }), 400
        
        url = data['url']
        
        # Basic URL validation
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return jsonify({
                'error': 'Invalid URL format',
                'status': 'error'
            }), 400
        
        return f(*args, **kwargs)
    return decorated_function

def log_performance(f):
    """Decorator for performance logging"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        end_time = time.time()
        
        logger.info(f"Function {f.__name__} took {end_time - start_time:.3f}s")
        return result
    return decorated_function

class RequestValidator:
    """Request validator"""
    
    @staticmethod
    def validate_scrape_request(data):
        """Validates scraping request"""
        errors = []
        
        if not isinstance(data, dict):
            errors.append("Request body must be JSON object")
            return errors
        
        if 'url' not in data:
            errors.append("URL field is required")
        elif not isinstance(data['url'], str):
            errors.append("URL must be a string")
        elif len(data['url']) > 2048:
            errors.append("URL too long (max 2048 characters)")
        
        # Optional validations
        if 'timeout' in data:
            try:
                timeout = int(data['timeout'])
                if timeout < 1 or timeout > 30:
                    errors.append("Timeout must be between 1 and 30 seconds")
            except (ValueError, TypeError):
                errors.append("Timeout must be an integer")
        
        return errors

class APIKeyAuth:
    """Simple API Key authentication (optional)"""
    
    def __init__(self, required_endpoints=None):
        self.required_endpoints = required_endpoints or []
        self.valid_keys = set()
        
        # Load valid keys from environment
        api_keys = os.environ.get('API_KEYS', '')
        if api_keys:
            self.valid_keys = set(api_keys.split(','))
    
    def require_api_key(self, f):
        """Decorator that requires API key"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not self.valid_keys:
                # If no keys are configured, allow access
                return f(*args, **kwargs)
            
            api_key = request.headers.get('X-API-Key')
            
            if not api_key:
                return jsonify({
                    'error': 'API key required',
                    'message': 'Include X-API-Key header',
                    'status': 'error'
                }), 401
            
            if api_key not in self.valid_keys:
                return jsonify({
                    'error': 'Invalid API key',
                    'status': 'error'
                }), 401
            
            return f(*args, **kwargs)
        return decorated_function