# Sport News Search System

A comprehensive Vietnamese sport news search system powered by Elasticsearch, featuring full-text search and automated web crawling capabilities.

## 🏗️ Architecture

This system consists of multiple microservices working together:

- **Frontend**: React + TypeScript + Material UI interface
- **Backend**: Sanic API server with Elasticsearch integration
- **Search Database**: Elasticsearch with custom Vietnamese language analyzers
- **Crawler**: Scrapy-based web crawler for sports news articles
- **Elasticsearch**: Optimized search engine with Vietnamese language support

## 🚀 Features

- **Full-Text Search**: Advanced multi-match search with BM25 ranking algorithm
- **Vietnamese Language Support**: Custom analyzers, tokenizers, and stopwords
- **Synonym & Antonym Support**: Domain-specific synonym mappings for sports terminology
- **Automated Crawling**: Scheduled crawling of Vietnamese sports news websites
- **Highlighting**: Search result highlighting for better user experience
- **RESTful API**: Well-documented API with OpenAPI/Swagger support
- **Docker Compose**: Easy deployment with container orchestration

## 📋 Prerequisites

- Docker and Docker Compose
- At least 4GB of RAM (for Elasticsearch)
- Node.js 18+ (for local frontend development)
- Python 3.10+ (for local backend development)

## 🛠️ Technology Stack

### Backend
- **Framework**: Sanic 24.6.0
- **Search Engine**: Elasticsearch 8.x
- **Web Crawler**: Scrapy 2.13.4
- **Validation**: Pydantic 1.10.12
- **HTTP Client**: aiohttp
- **Job Scheduler**: python-cli-scheduler

### Frontend
- **Framework**: React 19.1.1
- **Language**: TypeScript 5.8.3
- **Build Tool**: Vite 7.1.7
- **UI Library**: Material UI 7.3.4
- **Routing**: React Router DOM 7.9.4
- **Data Fetching**: TanStack Query 5.90.5
- **HTTP Client**: Axios 1.12.2

## 📦 Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd search-system
   ```

2. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   # Elasticsearch Configuration
   STACK_VERSION=8.11.0
   CLUSTER_NAME=search-cluster
   ES_PORT=9200
   ELASTIC_PASSWORD=changeme
   
   # Optional: Adjust based on your system
   ES_JAVA_OPTS=-Xms2g -Xmx2g
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Wait for services to be ready**
   
   The setup process will:
   - Start Elasticsearch (may take 1-2 minutes)
   - Initialize search database with custom analyzers
   - Start backend API server
   - Start frontend web server

5. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8080
   - API Documentation: http://localhost:8080/docs
   - Elasticsearch: http://localhost:9200

### Manual Setup

#### Backend Setup

```bash
cd backend
pip install -r requirements.txt

# Set environment variables
export ELASTICSEARCH_HOST=http://localhost:9200
export ELASTICSEARCH_USERNAME=elastic
export ELASTIC_PASSWORD=changeme

# Run the server
python main.py
```

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

#### Search Database Setup

```bash
cd search-db
pip install -r requirements.txt

# Initialize Elasticsearch indices and mappings
python setup.py
```

## 📖 API Documentation

### Search Endpoints

**Multi-Match Search**
```http
POST /elastic_search/multi-match-search
Content-Type: application/json

{
  "query": "bóng đá",
  "fields": ["title", "content"],
  "from": 0,
  "size": 10
}
```

**Ping Elasticsearch**
```http
GET /elastic_search/ping
```

**Save Document**
```http
POST /elastic_search/save-document/{index_name}
Content-Type: application/json

{
  "id": "article-1",
  "link": "https://example.com/article",
  "title": "Article Title",
  "content": "Article content...",
  "length": 1500,
  "last_updated": "2026-02-20T10:00:00"
}
```

For complete API documentation, visit http://localhost:8080/docs after starting the backend service.

## 🕷️ Web Crawler

The system includes a Scrapy-based crawler for sports news.

### Run the crawler manually:

```bash
cd backend
scrapy crawl sport_news -o data/sport_news.jsonl
```

### Run with scheduler:

```bash
python -m app.cli.jobs.sport_news_crawler --scheduler "^true@3600"
```

The scheduler format:
- `^true@3600`: Run immediately, then every 3600 seconds (1 hour)
- `^false@86400`: Don't run immediately, run every 24 hours

## 🔍 Search Features

### Vietnamese Language Support

The system includes:
- Custom Vietnamese stopwords filtering
- Vietnamese word tokenization
- Number-to-text mapping (một → 1, hai → 2, etc.)
- Sports-specific synonym mappings:
  - `thể thao, sport, thể dục`
  - `vận động viên, vđv, cầu thủ, siêu sao`
  - `bóng đá, đá bóng, túc cầu`
  - And many more...

### Search Algorithms

- **BM25 Similarity**: Customized for title (b=0.3, k1=1.5) and content (b=0.75, k1=1.2)
- **Highlighting**: Contextual snippets around matched terms

## 📁 Project Structure

```
search-system/
├── backend/              # Sanic API server
│   ├── app/
│   │   ├── apis/        # API blueprints
│   │   ├── cli/         # CLI commands and jobs
│   │   ├── crawler/     # Scrapy crawler
│   │   ├── dto/         # Data transfer objects
│   │   ├── services/    # Business logic
│   │   └── utils/       # Utility functions
│   ├── config.py        # Configuration
│   ├── main.py          # Application entry point
│   └── requirements.txt
├── frontend/            # React application
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API services
│   │   ├── views/       # Page views
│   │   └── types/       # TypeScript types
│   ├── package.json
│   └── vite.config.ts
├── search-db/           # Elasticsearch setup
│   ├── elastic_custom_template/  # Custom analyzers
│   ├── data/            # Sample data and stopwords
│   └── setup.py         # Index initialization
├── elasticsearch/       # ES Dockerfile and plugins
├── docker-compose.yml   # Service orchestration
└── README.md
```

## 🔧 Configuration

### Elasticsearch Configuration

Key performance settings (in docker-compose.yml):
- **Memory**: 3GB limit, 2GB JVM heap
- **Shards**: 1 primary, 0 replicas (single-node setup)
- **Refresh Interval**: 60s for better indexing performance
- **Circuit Breakers**: Configured to prevent OOM errors
- **Disk Watermarks**: 85% low, 90% high, 95% flood

### Backend Configuration

Edit `backend/config.py` to customize:
- Server host and port
- Elasticsearch connection
- CORS settings
- Logging configuration

## 🧪 Testing

### Test the search functionality:

```bash
# Using curl
curl -X POST http://localhost:8080/elastic_search/multi-match-search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "bóng đá việt nam",
    "fields": ["title", "content"],
    "size": 5
  }'
```

## 📊 Monitoring

### Check Elasticsearch health:

```bash
curl http://localhost:9200/_cluster/health?pretty
```

### View indices:

```bash
curl http://localhost:9200/_cat/indices?v
```

### Check document count:

```bash
curl http://localhost:9200/articles/_count
```

## 🐛 Troubleshooting

### Elasticsearch won't start
- Ensure you have at least 4GB of available RAM
- Check Docker memory limits: `docker stats`
- Increase vm.max_map_count on Linux:
  ```bash
  sudo sysctl -w vm.max_map_count=262144
  ```

### Backend can't connect to Elasticsearch
- Verify Elasticsearch is running: `docker ps`
- Check network connectivity between containers
- Verify environment variables in docker-compose.yml

### Frontend API calls fail
- Ensure backend is running on port 8080
- Check CORS configuration in backend
- Verify API base URL in frontend/src/services/const.ts

### Crawler not collecting data
- Check website availability
- Review Scrapy settings in backend/app/crawler/settings.py
- Check crawler logs for errors

## 📝 License

[Specify your license here]

## 👥 Contributors

[List contributors here]

## 🙏 Acknowledgments

- Elasticsearch for the powerful search engine
- Vietnamese NLP community for language resources
- Material UI for the beautiful component library

## 📮 Support

For issues, questions, or contributions, please create an issue in the repository.

---

**Built with ❤️ for Vietnamese sports enthusiasts**
