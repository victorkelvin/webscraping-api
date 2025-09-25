from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from urllib.parse import urlparse
from datetime import datetime
from scraper.web_scraper import WebScraper

scraper = WebScraper()
app = Flask(__name__)
CORS(app)

# loggin config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



@app.route('/')
def home():
    """Root endpoint with API info"""
    return jsonify({
        'message': 'Web Scraping API',
        'version': '1.0.0',
        'endpoints': {
            '/scrape': 'POST - Basic scraping of a web page',
            '/scrape/products': 'POST - Extract products from an e-commerce page',
            '/health': 'GET - API health check'
        },
        'author': 'Victor Kelvin',
        'documentation': 'https://github.com/victorkelvin/web-scraping-api'
    })

@app.route('/health')
def health():
    """Endpoint health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Web Scraping API'
    })

@app.route('/scrape', methods=['POST'])
def scrape_page():
    """Basic scraping of a web page"""
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                'error': 'URL is required',
                'status': 'error'
            }), 400
        
        url = data['url']
        
        # URL basic validation
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            return jsonify({
                'error': 'Invalid URL',
                'status': 'error'
            }), 400
        
        logger.info(f"Scrapiing: {url}")
        result = scraper.scrape_page_info(url)
        
        if result['status'] == 'error':
            return jsonify(result), 500
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Endpoint error at /scrape: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'status': 'error'
        }), 500

@app.route('/scrape/products', methods=['POST'])
def scrape_products():
    """Extract products from an e-commerce page"""
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                'error': 'URL is required',
                'status': 'error'
            }), 400
        
        url = data['url']
        
        # URL basic validation
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            return jsonify({
                'error': 'Invalid URL',
                'status': 'error'
            }), 400
        
        logger.info(f"Products Scraping at: {url}")
        result = scraper.scrape_products_generic(url)
        
        if result['status'] == 'error':
            return jsonify(result), 500
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Endpoint error at /scrape/products: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'status': 'error'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'status': 'error'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'status': 'error'
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)