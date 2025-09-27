# API Endpoints for Article Search System

This frontend expects the following API endpoints to be available on `localhost:8001`:

## Search Articles
- **Endpoint**: `GET /api/articles/search`
- **Parameters**:
  - `query` (string, required): Search query
  - `page` (number, optional): Page number (default: 1)
  - `limit` (number, optional): Results per page (default: 10)
  - `author` (string, optional): Filter by author
  - `tags` (array, optional): Filter by tags

- **Response**:
```json
{
  "articles": [
    {
      "id": "string",
      "title": "string",
      "content": "string",
      "author": "string",
      "publishedAt": "string (ISO date)",
      "tags": ["string"],
      "summary": "string"
    }
  ],
  "total": "number",
  "page": "number",
  "limit": "number"
}
```

## Get Article by ID
- **Endpoint**: `GET /api/articles/{id}`
- **Response**: Single article object (same structure as above)

## Example Backend Implementation

Your backend should handle CORS for the frontend running on `localhost:5173` (Vite default port).

### Sample Express.js implementation:
```javascript
const express = require('express');
const cors = require('cors');

const app = express();

app.use(cors({
  origin: 'http://localhost:5173'
}));

app.get('/api/articles/search', (req, res) => {
  const { query, page = 1, limit = 10 } = req.query;
  
  // Your search logic here
  const articles = []; // Your search results
  const total = 0; // Total count
  
  res.json({
    articles,
    total,
    page: parseInt(page),
    limit: parseInt(limit)
  });
});

app.get('/api/articles/:id', (req, res) => {
  const { id } = req.params;
  
  // Your article retrieval logic here
  const article = {}; // Your article data
  
  res.json(article);
});

app.listen(8001, () => {
  console.log('Backend running on localhost:8001');
});
```
