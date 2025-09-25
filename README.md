# 🕷️ Web Scraping API

A robust and flexible REST API for web scraping, built with Flask and BeautifulSoup. Perfect for programmatically and scalably extracting data from web pages.

## ✨ Features

- 🚀 **RESTful API** - Well-structured and documented endpoints
- 🛡️ **Error Handling** - Input validation and robust exception handling
- 🌐 **CORS Enabled** - Ready for use in frontend web applications
- 📦 **Containerized** - Docker-ready for deployment
- 🔍 **Smart Scraping** - Automatic extraction of e-commerce products
- 📝 **Full Logging** - Easy monitoring and debugging
- ⚡ **Performance** - Optimized headers and reusable sessions

## 🛠️ Technologies

- **Flask** - Minimal and flexible web framework
- **BeautifulSoup4** - Powerful HTML/XML parser
- **Requests** - Elegant HTTP client
- **Docker** - Containerization for deployment
- **Gunicorn** - WSGI server for production

## 📋 Prerequisites

- Python 3.8+
- pip
- Docker (optional)

## 🚀 Installation

### Local Installation

```bash
# Clone the repository
git clone https://github.com/victorkelvin/webscraping-api.git
cd webscraping-api

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Using Docker

```bash
# Build the image
docker build -t webscraping-api .

# Run the container
docker run -p 5000:5000 webscraping-api
```

## 📖 API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 🏠 GET `/`
General API information
```json
{
  "message": "Web Scraping API",
  "version": "1.0.0",
  "endpoints": {
    "/scrape": "POST - Basic scraping of a URL",
    "/scrape/products": "POST - Extracts products from an e-commerce page",
    "/health": "GET - API status"
  }
}
```

#### 💓 GET `/health`
API health check
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "service": "Web Scraping API"
}
```

#### 🔍 POST `/scrape`
Extracts basic information from a web page

**Request:**
```json
{
  "url": "https://example.com"
}
```

**Response:**
```json
{
  "url": "https://example.com",
  "title": "Example Domain",
  "description": "This domain is for use in illustrative examples",
  "images": [
    {
      "url": "https://example.com/image.jpg",
      "alt": "Example image",
      "title": "Example"
    }
  ],
  "links": [
    {
      "url": "https://example.com/link",
      "text": "More information...",
      "title": "Link title"
    }
  ],
  "headings": [
    {
      "level": 1,
      "text": "Example Domain"
    }
  ],
  "scraped_at": "2024-01-15T10:30:00.000Z",
  "status": "success"
}
```

#### 🛒 POST `/scrape/products`
Extracts products from e-commerce pages

**Request:**
```json
{
  "url": "https://shop.example.com/products"
}
```

**Response:**
```json
{
  "url": "https://shop.example.com/products",
  "products": [
    {
      "name": "Product Name",
      "price": "R$ 99,90",
      "image": "https://shop.example.com/product-image.jpg",
      "link": "https://shop.example.com/product/123"
    }
  ],
  "total_found": 15,
  "scraped_at": "2024-01-15T10:30:00.000Z",
  "status": "success"
}
```

## 🧪 Testing the API

### Using the included test script:

```bash
python test_api.py
```

### Using curl:

```bash
# Health check
curl http://localhost:5000/health

# Basic scraping
curl -X POST http://localhost:5000/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://httpbin.org/html"}'

# Product scraping
curl -X POST http://localhost:5000/scrape/products \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example-shop.com"}'
```

### Using Python:

```python
import requests

# Basic scraping
response = requests.post('http://localhost:5000/scrape', 
                        json={'url': 'https://example.com'})
print(response.json())

# Product scraping
response = requests.post('http://localhost:5000/scrape/products', 
                        json={'url': 'https://shop.example.com'})
print(response.json())
```

## 🔧 Configuration

### Environment Variables

- `FLASK_ENV` - Application environment (development/production)
- `PORT` - Application port (default: 5000)

### Custom Headers

The API uses optimized headers to avoid blocking:
```python
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
```

## 🎯 Use Cases

- **Price Monitoring** - Track product prices on e-commerce sites
- **Competitor Analysis** - Collect data from competitor sites
- **Content Aggregation** - Compile information from multiple sources
- **SEO Analysis** - Extract metadata and page structure
- **Lead Generation** - Collect contact information from websites

## ⚠️ Limitations and Considerations

- **Rate Limiting** - Respect site limits
- **robots.txt** - Check scraping policies
- **JavaScript** - This API does not execute JavaScript (use Selenium for SPAs)
- **Timeout** - Requests have a 10-second timeout
- **Legal** - Only use on sites where you have permission

## 🤝 Contributing

1. Fork the project
2. Create a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 Project Structure

```
webscraping-api/
├── app.py              
├── scraper/
│   ├── __init__.py
│   └── web_scraper.py  
├── tests/
│   ├── test_app.py
│   └── test_scraper.py
└── requirements.txt
```

## 📝 License

This project is under the MIT license. See the `LICENSE` file for more details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@victorkelvin](https://github.com/victorkelvin)
- LinkedIn: [Victor Kelvin](https://linkedin.com/in/victor-kelvin)
- Email: victorkelvin@gmail.com

## 📊 Roadmap

- [ ] JWT Authentication
- [ ] IP-based rate limiting
- [ ] Redis cache
- [ ] JavaScript support (Selenium)
- [ ] Webhooks for notifications
- [ ] Web dashboard for monitoring

---

⭐ If this project was useful to you, consider giving it a star!

📫 Have any questions? Open an [issue](https://github.com/victorkelvin/webscraping-api/issues)!