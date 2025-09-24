# 🕷️ Web Scraping API

Uma API REST robusta e flexível para web scraping, construída com Flask e BeautifulSoup. Perfeita para extrair dados de páginas web de forma programática e escalável.

## ✨ Características

- 🚀 **API RESTful** - Endpoints bem estruturados e documentados
- 🛡️ **Tratamento de Erros** - Validação de entrada e tratamento robusto de exceções
- 🌐 **CORS Habilitado** - Pronto para uso em aplicações web frontend
- 📦 **Containerizado** - Docker pronto para deployment
- 🔍 **Scraping Inteligente** - Extração automática de produtos de e-commerce
- 📝 **Logging Completo** - Monitoramento e debugging facilitados
- ⚡ **Performance** - Headers otimizados e sessões reutilizáveis

## 🛠️ Tecnologias

- **Flask** - Framework web minimalista e flexível
- **BeautifulSoup4** - Parser HTML/XML poderoso
- **Requests** - Cliente HTTP elegante
- **Docker** - Containerização para deployment
- **Gunicorn** - Servidor WSGI para produção

## 📋 Pré-requisitos

- Python 3.8+
- pip
- Docker (opcional)

## 🚀 Instalação

### Instalação Local

```bash
# Clone o repositório
git clone https://github.com/victorkelvin/webscraping-api.git
cd webscraping-api

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python app.py
```

### Usando Docker

```bash
# Build da imagem
docker build -t webscraping-api .

# Execute o container
docker run -p 5000:5000 webscraping-api
```

## 📖 Documentação da API

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 🏠 GET `/`
Informações gerais da API
```json
{
  "message": "Web Scraping API",
  "version": "1.0.0",
  "endpoints": {
    "/scrape": "POST - Faz scraping básico de uma URL",
    "/scrape/products": "POST - Extrai produtos de uma página de e-commerce",
    "/health": "GET - Status da API"
  }
}
```

#### 💓 GET `/health`
Health check da API
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "service": "Web Scraping API"
}
```

#### 🔍 POST `/scrape`
Extrai informações básicas de uma página web

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
Extrai produtos de páginas de e-commerce

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

## 🧪 Testando a API

### Usando o script de teste incluído:

```bash
python test_api.py
```

### Usando curl:

```bash
# Health check
curl http://localhost:5000/health

# Scraping básico
curl -X POST http://localhost:5000/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://httpbin.org/html"}'

# Scraping de produtos
curl -X POST http://localhost:5000/scrape/products \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example-shop.com"}'
```

### Usando Python:

```python
import requests

# Scraping básico
response = requests.post('http://localhost:5000/scrape', 
                        json={'url': 'https://example.com'})
print(response.json())

# Scraping de produtos
response = requests.post('http://localhost:5000/scrape/products', 
                        json={'url': 'https://shop.example.com'})
print(response.json())
```

## 🔧 Configuração

### Variáveis de Ambiente

- `FLASK_ENV` - Ambiente da aplicação (development/production)
- `PORT` - Porta da aplicação (default: 5000)

### Headers Personalizados

A API usa headers otimizados para evitar bloqueios:
```python
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
```

## 🚀 Deploy

### Heroku

```bash
# Instale o Heroku CLI e faça login
heroku create sua-api-webscraping

# Deploy
git push heroku main
```

### Railway/Render

1. Conecte seu repositório GitHub
2. Configure as variáveis de ambiente
3. Deploy automático

## 🎯 Casos de Uso

- **Monitoramento de Preços** - Acompanhe preços de produtos em e-commerce
- **Análise de Concorrência** - Colete dados de sites concorrentes
- **Agregação de Conteúdo** - Compile informações de múltiplas fontes
- **SEO Analysis** - Extraia metadados e estrutura de páginas
- **Lead Generation** - Colete informações de contato de websites

## ⚠️ Limitações e Considerações

- **Rate Limiting** - Respeite os limites dos sites
- **robots.txt** - Verifique as políticas de scraping
- **JavaScript** - Esta API não executa JavaScript (use Selenium para SPAs)
- **Timeout** - Requests têm timeout de 10 segundos
- **Legal** - Use apenas em sites onde você tem permissão

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Estrutura do Projeto

```
webscraping-api/
├── app.py              # Aplicação principal
├── requirements.txt    # Dependências
├── Dockerfile         # Configuração Docker
├── test_api.py        # Scripts de teste
├── README.md          # Documentação
└── .gitignore         # Arquivos ignorados
```

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

**Seu Nome**
- GitHub: [@seu-usuario](https://github.com/seu-usuario)
- LinkedIn: [Seu LinkedIn](https://linkedin.com/in/seu-perfil)
- Email: seu.email@example.com

## 📊 Roadmap

- [ ] Autenticação JWT
- [ ] Rate limiting por IP
- [ ] Cache Redis
- [ ] Suporte a JavaScript (Selenium)
- [ ] Webhooks para notificações
- [ ] Dashboard web para monitoramento

---

⭐ Se este projeto foi útil para você, considere dar uma estrela!

📫 Tem alguma dúvida? Abra uma [issue](https://github.com/seu-usuario/webscraping-api/issues)!