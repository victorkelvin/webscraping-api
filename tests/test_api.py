import requests
import json
import time
import random

# API base URL
BASE_URL = "http://localhost:5000"

def test_health():
    """Tests the health check endpoint"""
    print("🔍 Testing Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print("-" * 50)

def test_basic_scraping():
    """Tests basic scraping"""
    print("🔍 Testing Basic Scraping...")
    
    # Test with an example site
    payload = {
        "url": "https://httpbin.org/html"
    }
    
    response = requests.post(f"{BASE_URL}/scrape", json=payload, timeout=60)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Title: {data.get('title', 'N/A')}")
        print(f"Description: {data.get('description', 'N/A')}")
        print(f"Total links: {len(data.get('links', []))}")
        print(f"Total images: {len(data.get('images', []))}")
        print(f"Total headings: {len(data.get('headings', []))}")
        if data.get('headings'):
            print(f"Heading: {data['headings'][0].get('text', 'N/A')}")
    else:
        print(f"Error: {response.text}")
    
    print("-" * 50)

def test_product_scraping():
    """Tests product scraping"""
    print("🔍 Testing Product Scraping...")
    
    # Test with an example page with e-commerce-like structure
    payload = {
        "url": "https://books.toscrape.com/"
    }
    
    response = requests.post(f"{BASE_URL}/scrape/products", json=payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total products found: {data.get('total_found', 0)}")
        
        for i, product in enumerate(data.get('products', [])[:3]): 
            print(f"Product {i+1}:")
            print(f"  Name: {product.get('name', 'N/A')}")
            print(f"  Price: {product.get('price', 'N/A')}")
            print(f"  Link: {product.get('link', 'N/A')}")
    else:
        print(f"Error: {response.text}")
    
    print("-" * 50)

def test_error_handling():
    """Tests error handling"""
    print("🔍 Testing Error Handling...")
    
    # Test with invalid URL
    payload = {
        "url": "invalid-url"
    }
    
    response = requests.post(f"{BASE_URL}/scrape", json=payload)
    print(f"Status (invalid URL): {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # Test without URL
    response = requests.post(f"{BASE_URL}/scrape", json={})
    print(f"Status (no URL): {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    print("-" * 50)

if __name__ == "__main__":
    print("🚀 Starting Web Scraping API Tests\n")
    
    try:
        test_health()
        test_basic_scraping()
        test_product_scraping()
        test_error_handling()
        
        print("✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API.")
        print("Make sure the API is running at http://localhost:5000")
    except Exception as e:
        print(f"❌ Error during tests: {str(e)}")