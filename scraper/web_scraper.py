import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_page_info(self, url):
        """Extract basic page information"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # basic info
            title = soup.find('title')
            title = title.get_text().strip() if title else "Sem título"
            
            description = soup.find('meta', attrs={'name': 'description'})
            description = description.get('content', '').strip() if description else "No description"
            
            # Searching for images
            images = []
            for img in soup.find_all('img', src=True):
                img_url = urljoin(url, img['src'])
                images.append({
                    'url': img_url,
                    'alt': img.get('alt', ''),
                    'title': img.get('title', '')
                })
            
            # Searching for links
            links = []
            for link in soup.find_all('a', href=True):
                link_url = urljoin(url, link['href'])
                links.append({
                    'url': link_url,
                    'text': link.get_text().strip(),
                    'title': link.get('title', '')
                })
            
            # Extracting headings
            headings = []
            for i in range(1, 7):
                for heading in soup.find_all(f'h{i}'):
                    headings.append({
                        'level': i,
                        'text': heading.get_text().strip()
                    })
            
            return {
                'url': url,
                'title': title,
                'description': description,
                'images': images[:10],  
                'links': links[:20],    
                'headings': headings,
                'scraped_at': datetime.now().isoformat(),
                'status': 'success'
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Scraping error at {url}: {str(e)}")
            return {
                'url': url,
                'error': str(e),
                'status': 'error',
                'scraped_at': datetime.now().isoformat()
            }
    
    def scrape_products_generic(self, url):
        """Try to extract products from a generic e-commerce page"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            products = []
            
            # Common product selectors
            product_selectors = [
                '[class*="product"]',
                '[id*="product"]',
                '[data-product-id]',
                '.item',
            ]
            
            for selector in product_selectors:
                product_elements = soup.select(selector)
                if product_elements:
                    for element in product_elements[:10]:  # limit to first 10 products
                        product = self.extract_product_info(element, url)
                        if product:
                            products.append(product)
                    break
            
            return {
                'url': url,
                'products': products,
                'total_found': len(products),
                'scraped_at': datetime.now().isoformat(),
                'status': 'success'
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Scraping error at {url}: {str(e)}")
            return {
                'url': url,
                'error': str(e),
                'status': 'error',
                'scraped_at': datetime.now().isoformat()
            }
    
    def extract_product_info(self, element, base_url):
        """Extract product info from a BeautifulSoup element"""
        try:
            # Try to find product name
            name_selectors = [
                'h1', 'h2', 'h3',
                '[class*="title"]', '[class*="name"]', '[class*="product-name"]', '[class*="product-title"]',
                '[id*="title"]', '[id*="name"]', '[id*="product-name"]', '[id*="product-title"]'
            ]
            name = ""
            for selector in name_selectors:
                name_elem = element.select_one(selector)
                if name_elem:
                    name = name_elem.get_text().strip()
                    break

            # Try to find price
            price_selectors = [
                '[class*="price"]', '[id*="price"]', '[data-price]',
                '[class*="cost"]', '[id*="cost"]',
                '[class*="amount"]', '[id*="amount"]',
                '.product-price', '.price', '.cost', '.amount'
            ]
            price = ""
            for selector in price_selectors:
                price_elem = element.select_one(selector)
                if price_elem:
                    price_text = price_elem.get_text().strip()
                    price_match = re.search(r'([A-Za-z]{0,3}\$|€|£|¥|₹)\s*[\d.,]+', price_text)
                    if price_match:
                        price = price_match.group()
                        break

            # Try to find image
            image_selectors = [
                'img', '[class*="image"] img', '[class*="img"] img',
                '[class*="product-image"] img', '[class*="thumb"] img',
                '[data-src]', '[data-original]'
            ]
            image = ""
            for selector in image_selectors:
                img_elem = element.select_one(selector)
                if img_elem:
                    src = img_elem.get('src') or img_elem.get('data-src') or img_elem.get('data-original')
                    if src:
                        image = urljoin(base_url, src)
                        break

            # Try to find product link
            link_selectors = [
                'a[href]', '[class*="link"] a[href]', '[class*="product-link"] a[href]',
                '[class*="title"] a[href]', '[class*="name"] a[href]'
            ]
            link = ""
            for selector in link_selectors:
                link_elem = element.select_one(selector)
                if link_elem:
                    link = urljoin(base_url, link_elem.get('href'))
                    break

            if name:
                return {
                    'name': name,
                    'price': price,
                    'image': image,
                    'link': link
                }

        except Exception as e:
            logger.error(f"Error at extract product information: {str(e)}")

        return None

scraper = WebScraper()