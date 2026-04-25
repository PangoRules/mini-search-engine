# Mini Search Engine API Documentation

## Search Endpoint

### Endpoint
`GET /search`

### Parameters
- `q` (required): Search query string
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Number of results per page (default: 10, max: 50)

### Response Format
```json
{
  "query": "search query",
  "page": 1,
  "page_size": 10,
  "total_results": 5,
  "total_pages": 1,
  "results": [
    {
      "title": "Page Title",
      "url": "https://example.com",
      "snippet": "First few words of content",
      "score": 0.95
    }
  ]
}
```

### Error Codes
- `429 Too Many Requests`: Rate limiting exceeded