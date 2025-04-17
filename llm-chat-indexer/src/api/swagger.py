"""
Swagger documentation for the LLM Chat Indexer API.

This module provides Swagger/OpenAPI documentation for the API endpoints
using Flask-Swagger-UI and apispec.
"""

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_swagger_ui import get_swaggerui_blueprint

# Create an APISpec
spec = APISpec(
    title="LLM Chat Indexer API",
    version="1.0.0",
    openapi_version="3.0.2",
    info=dict(
        description="API for indexing, searching, and analyzing chat conversations with LLMs",
        contact=dict(email="your.email@example.com"),
        license=dict(name="MIT"),
    ),
    plugins=[MarshmallowPlugin()],
)

# Define schemas
spec.components.schema(
    "Error",
    {
        "type": "object",
        "properties": {
            "error": {"type": "string", "description": "Error message"},
        },
        "required": ["error"],
    },
)

spec.components.schema(
    "Summary",
    {
        "type": "object",
        "properties": {
            "summary": {"type": "string", "description": "Generated summary of the chat"},
        },
        "required": ["summary"],
    },
)

spec.components.schema(
    "GraphData",
    {
        "type": "object",
        "properties": {
            "nodes": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "type": {"type": "string"},
                        "attributes": {"type": "object"},
                    },
                },
            },
            "links": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "source": {"type": "string"},
                        "target": {"type": "string"},
                        "type": {"type": "string"},
                        "attributes": {"type": "object"},
                    },
                },
            },
        },
        "required": ["nodes", "links"],
    },
)

# Define routes
spec.path(
    path="/upload",
    operations={
        "post": {
            "tags": ["Chat Management"],
            "summary": "Upload and index a chat file",
            "description": "Uploads a JSON or Markdown file containing chat data and indexes it for searching",
            "requestBody": {
                "content": {
                    "multipart/form-data": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "file": {
                                    "type": "string",
                                    "format": "binary",
                                    "description": "Chat file to upload (JSON or Markdown)",
                                },
                            },
                            "required": ["file"],
                        }
                    }
                }
            },
            "responses": {
                "302": {
                    "description": "Redirect to chat view page",
                },
                "400": {
                    "description": "Bad request",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Error"}
                        }
                    },
                },
            },
        }
    },
)

spec.path(
    path="/chat/{chat_id}",
    operations={
        "get": {
            "tags": ["Chat Management"],
            "summary": "View a specific chat",
            "description": "Returns the HTML page for viewing a specific chat",
            "parameters": [
                {
                    "name": "chat_id",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string"},
                    "description": "ID of the chat to view",
                }
            ],
            "responses": {
                "200": {
                    "description": "HTML page with chat data",
                },
                "404": {
                    "description": "Chat not found",
                },
            },
        }
    },
)

spec.path(
    path="/search",
    operations={
        "get": {
            "tags": ["Search"],
            "summary": "Search indexed chats",
            "description": "Searches indexed chats for the given query",
            "parameters": [
                {
                    "name": "query",
                    "in": "query",
                    "required": True,
                    "schema": {"type": "string"},
                    "description": "Search query",
                },
                {
                    "name": "chat_id",
                    "in": "query",
                    "required": False,
                    "schema": {"type": "string"},
                    "description": "Limit search to a specific chat",
                },
            ],
            "responses": {
                "200": {
                    "description": "HTML page with search results",
                },
                "400": {
                    "description": "Bad request",
                },
            },
        }
    },
)

spec.path(
    path="/summary/{chat_id}",
    operations={
        "get": {
            "tags": ["Summarization"],
            "summary": "Generate a summary for a chat",
            "description": "Generates a summary for a specific chat",
            "parameters": [
                {
                    "name": "chat_id",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string"},
                    "description": "ID of the chat to summarize",
                },
                {
                    "name": "type",
                    "in": "query",
                    "required": False,
                    "schema": {"type": "string", "enum": ["gist", "key_points"]},
                    "description": "Type of summary to generate",
                    "default": "gist",
                },
            ],
            "responses": {
                "200": {
                    "description": "Summary generated successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Summary"}
                        }
                    },
                },
                "404": {
                    "description": "Chat not found",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Error"}
                        }
                    },
                },
                "500": {
                    "description": "Server error",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Error"}
                        }
                    },
                },
            },
        }
    },
)

spec.path(
    path="/api/graph/{chat_id}",
    operations={
        "get": {
            "tags": ["Knowledge Graph"],
            "summary": "Get knowledge graph data",
            "description": "Returns the knowledge graph data for a specific chat",
            "parameters": [
                {
                    "name": "chat_id",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string"},
                    "description": "ID of the chat",
                },
                {
                    "name": "format",
                    "in": "query",
                    "required": False,
                    "schema": {"type": "string", "enum": ["json", "cytoscape"]},
                    "description": "Format of the graph data",
                    "default": "json",
                },
            ],
            "responses": {
                "200": {
                    "description": "Graph data retrieved successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/GraphData"}
                        }
                    },
                },
                "404": {
                    "description": "Chat not found",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Error"}
                        }
                    },
                },
                "500": {
                    "description": "Server error",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Error"}
                        }
                    },
                },
            },
        }
    },
)

# Generate the OpenAPI specification
swagger_spec = spec.to_dict()

# Create Swagger UI Blueprint
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI
API_URL = '/api/swagger.json'  # URL for getting OpenAPI spec

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "LLM Chat Indexer API",
        'dom_id': '#swagger-ui',
        'deepLinking': True,
        'layout': 'BaseLayout',
        'defaultModelsExpandDepth': 1,
        'defaultModelExpandDepth': 1,
    },
)
