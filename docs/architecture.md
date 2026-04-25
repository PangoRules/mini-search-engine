# Mini Search Engine Architecture

## Overview

This search engine follows a layered architecture approach where:

1. **Data Ingestion Layer** - Web crawler and document processing
2. **Storage Layer** - SQLite database for persisting documents and indices
3. **Indexing Layer** - Inverted index and TF-IDF scoring 
4. **Search Layer** - Rank results based on relevance and authority
5. **API Layer** - Exposes search functionality via RESTful API

## Components

### Web Crawler
- Crawls pages from seed URLs using BFS approach
- Respects robots.txt and domain filtering
- Handles crawling depth limits
- Normalizes URLs for consistent storage
- Logs crawl activities with structured logging

### Index Builder
- Builds inverted index of words to documents
- Calculates term frequency for documents
- Uses TF-IDF scoring
- Combines text relevance with PageRank authority scores
- Logs indexing operations with structured logging

### Search Engine
- Handles user search queries
- Ranks documents using combined TF-IDF + PageRank
- Returns paginated results with snippets
- Supports rate limiting
- Logs search activities with structured logging

### API Layer
- Exposes search functionality via RESTful API
- Handles request validation and error responses
- Provides swagger UI for testing
- Logs API activities with structured logging

## Data Flow

1. Crawling phase: Web crawler fetches pages and stores them in database
2. Indexing phase: Inverted index is built from stored pages
3. Search phase: Users query the search engine with TF-IDF + authority scoring
4. API phase: Results are returned via RESTful interface with structured logging

## Logging Structure

All modules use structured JSON logging with consistent format:
- Timestamp of log entry
- Log level (DEBUG, INFO, WARNING, ERROR)
- Component name (crawler, index_builder, etc.)
- Message content
- Additional context information as key-value pairs