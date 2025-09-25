"""
Automated test suite for the Web Scraping API
"""

import unittest
import requests
import json
import time
from unittest.mock import patch, Mock
import sys
import os

# Add root directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app, WebScraper
except ImportError:
    print("❌ Error: Could not import the application")
    sys.exit(1)

class TestWebScrapingAPI(unittest.TestCase):
    """Tests for the Web Scraping API"""
    
    @classmethod
    def setUpClass(cls):
        """Initial setup for all tests"""
        cls.base_url = "http://localhost:5000"
        cls.app = app.test_client()
        cls.app.testing = True
    
    def test_health_endpoint(self):
        """Tests the health check endpoint"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('timestamp', data)
        self.assertIn('service', data)
    
    def test_root_endpoint(self):
        """Tests the root endpoint"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('version', data)
        self.assertIn('endpoints', data)
    
    def test_scrape_endpoint_valid_url(self):
        """Tests scraping with a valid URL"""
        test_payload = {"url": "https://httpbin.org/html"}
        
        response = self.app.post('/scrape',
                               data=json.dumps(test_payload),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('title', data)
        self.assertIn('scraped_at', data)
    
    def test_scrape_endpoint_invalid_url(self):
        """Tests scraping with an invalid URL"""
        test_payload = {"url": "invalid-url"}
        
        response = self.app.post('/scrape',
                               data=json.dumps(test_payload),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
    
    def test_scrape_endpoint_missing_url(self):
        """Tests scraping without a URL"""
        test_payload = {}
        
        response = self.app.post('/scrape',
                               data=json.dumps(test_payload),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('URL is required', data['error'])
    
    def test_products_endpoint_valid_url(self):
        """Tests product scraping with a valid URL"""
        test_payload = {"url": "https://httpbin.org/html"}
        
        response = self.app.post('/scrape/products',
                               data=json.dumps(test_payload),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('products', data)
        self.assertIn('total_found', data)
    
    def test_404_handler(self):
        """Tests the handler for not found endpoints"""
        response = self.app.get('/nonexistent-endpoint')
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')

class TestWebScraper(unittest.TestCase):
    """Tests for the WebScraper class"""
    
    def setUp(self):
        """Setup for each test"""
        self.scraper = WebScraper()
    
    @patch('requests.Session.get')
    def test_scrape_page_info_success(self, mock_get):
        """Tests successful scraping"""
        # Mock HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'''
        <html>
            <head>
                <title>Test Page</title>
                <meta name="description" content="Test description">
            </head>
            <body>
                <h1>Main Heading</h1>
                <a href="/link1">Link 1</a>
                <img src="/image1.jpg" alt="Image 1">
            </body>
        </html>
        '''
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.scraper.scrape_page_info("https://example.com")
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['title'], 'Test Page')
        self.assertEqual(result['description'], 'Test description')
        self.assertTrue(len(result['headings']) > 0)
        self.assertTrue(len(result['links']) > 0)
        self.assertTrue(len(result['images']) > 0)
    
    @patch('requests.Session.get')
    def test_scrape_page_info_error(self, mock_get):
        """Tests error handling in scraping"""
        # Mock connection error
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        result = self.scraper.scrape_page_info("https://example.com")
        
        self.assertEqual(result['status'], 'error')
        self.assertIn('error', result)
    
    def test_extract_product_info(self):
        """Tests product information extraction"""
        from bs4 import BeautifulSoup
        
        html = '''
        <div class="product">
            <h2>Test Product</h2>
            <span class="price">R$ 99,90</span>
            <img src="/product.jpg" alt="Product">
            <a href="/product/123">View Product</a>
        </div>
        '''
        
        soup = BeautifulSoup(html, 'html.parser')
        product_element = soup.find('div', class_='product')
        
        result = self.scraper.extract_product_info(product_element, "https://example.com")
        
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'Test Product')
        self.assertEqual(result['price'], 'R$ 99,90')
        self.assertIn('product.jpg', result['image'])
        self.assertIn('/product/123', result['link'])

class TestAPIIntegration(unittest.TestCase):
    """API integration tests (requires API running)"""
    
    @classmethod
    def setUpClass(cls):
        """Checks if the API is running"""
        try:
            response = requests.get("http://localhost:5000/health", timeout=5)
            if response.status_code != 200:
                raise Exception("API is not responding")
            cls.api_available = True
        except:
            cls.api_available = False
    
    def setUp(self):
        """Skips tests if the API is not available"""
        if not self.api_available:
            self.skipTest("API is not running on localhost:5000")
    
    def test_full_scraping_workflow(self):
        """Tests the full scraping workflow"""
        # Test with a site we know works
        payload = {"url": "https://httpbin.org/html"}
        
        response = requests.post("http://localhost:5000/scrape", 
                               json=payload, timeout=10)
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('title', data)
        self.assertIn('scraped_at', data)
    
    def test_rate_limiting_behavior(self):
        """Tests behavior with multiple requests"""
        payload = {"url": "https://httpbin.org/html"}
        
        # Make multiple requests quickly
        responses = []
        for i in range(3):
            response = requests.post("http://localhost:5000/scrape", 
                                   json=payload, timeout=10)
            responses.append(response.status_code)
            time.sleep(0.1)  # Small pause
        
        # All requests should succeed
        for status_code in responses:
            self.assertEqual(status_code, 200)

class TestPerformance(unittest.TestCase):
    """Performance tests"""
    
    def setUp(self):
        self.scraper = WebScraper()
    
    @patch('requests.Session.get')
    def test_scraping_performance(self, mock_get):
        """Tests if scraping executes in a reasonable time"""
        # Mock large response
        large_content = "<html><body>" + "<div>Content</div>" * 1000 + "</body></html>"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = large_content.encode()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        start_time = time.time()
        result = self.scraper.scrape_page_info("https://example.com")
        end_time = time.time()
        
        # Should complete in less than 5 seconds
        self.assertLess(end_time - start_time, 5.0)
        self.assertEqual(result['status'], 'success')

def run_test_suite():
    """Runs all tests with detailed report"""
    print("🧪 RUNNING TEST SUITE")
    print("=" * 60)
    
    # Discover all tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    # Run tests with verbosity
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(suite)
    
    # Final report
    print("\n" + "=" * 60)
    print("📊 FINAL TEST REPORT")
    print(f"✅ Tests run: {result.testsRun}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"🚫 Errors: {len(result.errors)}")
    print(f"⏭️  Skipped: {len(result.skipped)}")
    
    if result.failures:
        print("\n🔴 FAILURES:")
        for test, traceback in result.failures:
            print(f"  • {test}: {traceback.split('AssertionError: ')[-1].split(chr(10))[0]}")
    
    if result.errors:
        print("\n🔴 ERRORS:")
        for test, traceback in result.errors:
            print(f"  • {test}: {traceback.split(chr(10))[-2]}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0
    print(f"\n🎯 Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("🏆 EXCELLENT! API ready for production!")
    elif success_rate >= 75:
        print("👍 GOOD! Some adjustments may be needed.")
    else:
        print("⚠️  ATTENTION! Review code before deployment.")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_test_suite()
    sys.exit(0 if success else 1)