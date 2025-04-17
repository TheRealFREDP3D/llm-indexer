# API Documentation

This document provides detailed information about the LLM Chat Indexer API endpoints.

## Base URL

All API endpoints are relative to the base URL of your LLM Chat Indexer instance:

```
http://localhost:5000
```

## Authentication

Currently, the API does not require authentication. This may change in future versions.

## Endpoints

### Chat Management

#### Upload a Chat

```
POST /upload
```

Uploads and indexes a chat file.

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `file`: The chat file to upload (JSON or Markdown)

**Response:**
- Success: Redirects to `/chat/{chat_id}`
- Error: Redirects to `/` with an error message

**Example:**
```bash
curl -X POST -F "file=@sample_chat.json" http://localhost:5000/upload
```

#### View a Chat

```
GET /chat/{chat_id}
```

Returns the HTML page for viewing a specific chat.

**Parameters:**
- `chat_id`: The ID of the chat to view

**Response:**
- Success: HTML page with chat data
- Error: Redirects to `/` with an error message

**Example:**
```bash
curl http://localhost:5000/chat/24f0b044-aae3-47e3-a294-afbad939cd24
```

### Search

#### Search Chats

```
GET /search
```

Searches indexed chats for the given query.

**Parameters:**
- `query`: The search query
- `chat_id` (optional): Limit search to a specific chat

**Response:**
- Success: HTML page with search results
- Error: HTML page with error message

**Example:**
```bash
curl http://localhost:5000/search?query=renewable+energy
```

### Summarization

#### Generate Summary

```
GET /summary/{chat_id}
```

Generates a summary for a specific chat.

**Parameters:**
- `chat_id`: The ID of the chat to summarize
- `type` (optional): The type of summary to generate (`gist` or `key_points`). Default: `gist`

**Response:**
- Success: JSON object with the summary
  ```json
  {
    "summary": "This is a summary of the chat..."
  }
  ```
- Error: JSON object with error message
  ```json
  {
    "error": "Error message..."
  }
  ```

**Example:**
```bash
curl http://localhost:5000/summary/24f0b044-aae3-47e3-a294-afbad939cd24?type=key_points
```

### Knowledge Graph

#### Get Graph Data

```
GET /api/graph/{chat_id}
```

Returns the knowledge graph data for a specific chat.

**Parameters:**
- `chat_id`: The ID of the chat
- `format` (optional): The format of the graph data (`json` or `cytoscape`). Default: `json`

**Response:**
- Success: JSON object with graph data
  ```json
  {
    "nodes": [...],
    "links": [...]
  }
  ```
- Error: JSON object with error message
  ```json
  {
    "error": "Error message..."
  }
  ```

**Example:**
```bash
curl http://localhost:5000/api/graph/24f0b044-aae3-47e3-a294-afbad939cd24?format=json
```

## Data Formats

### Chat Data

Chat data can be uploaded in the following formats:

#### JSON Format

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hello, how are you?",
      "timestamp": "2023-01-01T12:00:00Z"
    },
    {
      "role": "assistant",
      "content": "I'm doing well, thank you for asking!",
      "timestamp": "2023-01-01T12:00:05Z"
    }
  ]
}
```

#### Markdown Format

```markdown
# Chat Session

**User**: Hello, how are you?

**Assistant**: I'm doing well, thank you for asking!
```

### Knowledge Graph Data

Knowledge graph data is returned in the following formats:

#### JSON Format

```json
{
  "nodes": [
    {
      "id": "1",
      "name": "John Smith",
      "type": "person",
      "attributes": {}
    },
    {
      "id": "2",
      "name": "Microsoft",
      "type": "organization",
      "attributes": {}
    }
  ],
  "links": [
    {
      "source": "1",
      "target": "2",
      "type": "works_at",
      "attributes": {}
    }
  ]
}
```

#### Cytoscape Format

```json
{
  "elements": {
    "nodes": [
      {
        "data": {
          "id": "1",
          "name": "John Smith",
          "type": "person"
        }
      },
      {
        "data": {
          "id": "2",
          "name": "Microsoft",
          "type": "organization"
        }
      }
    ],
    "edges": [
      {
        "data": {
          "id": "e1",
          "source": "1",
          "target": "2",
          "label": "works_at"
        }
      }
    ]
  }
}
```

## Error Handling

All API endpoints return appropriate HTTP status codes:

- `200 OK`: The request was successful
- `400 Bad Request`: The request was invalid
- `404 Not Found`: The requested resource was not found
- `500 Internal Server Error`: An error occurred on the server

JSON error responses have the following format:

```json
{
  "error": "Error message..."
}
```

## Rate Limiting

Currently, there are no rate limits on API requests. This may change in future versions.

## Versioning

The API is currently at version 1.0. Future versions will be announced with appropriate migration guides.
