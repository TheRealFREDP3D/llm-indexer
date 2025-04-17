# LLM Chat Indexer User Guide

This guide provides detailed instructions for using the LLM Chat Indexer application.

## Table of Contents

- [Getting Started](#getting-started)
- [Uploading Chats](#uploading-chats)
- [Searching Chats](#searching-chats)
- [Viewing Chats](#viewing-chats)
- [Generating Summaries](#generating-summaries)
- [Exploring Knowledge Graphs](#exploring-knowledge-graphs)
- [Troubleshooting](#troubleshooting)

## Getting Started

### Accessing the Application

1. Ensure the application is running (see the [Setup Guide](../SETUP.md) for installation instructions)
2. Open your web browser and navigate to `http://localhost:5000`
3. You should see the LLM Chat Indexer homepage with a list of indexed chats (if any) and an upload form

### Understanding the Interface

The main interface consists of:

- **Navigation Bar**: At the top of every page, with links to the home page and search functionality
- **Chat List**: On the home page, showing all indexed chats
- **Upload Form**: On the home page, for adding new chats
- **Search Bar**: In the navigation bar, for searching across all indexed chats

## Uploading Chats

### Supported File Formats

The application supports two file formats:

#### JSON Format

JSON files should have a `messages` array containing objects with `role` and `content` fields:

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

The `timestamp` field is optional but recommended for better organization.

#### Markdown Format

Markdown files should have messages formatted with role headers:

```markdown
# Chat Session

**User**: Hello, how are you?

**Assistant**: I'm doing well, thank you for asking!
```

Alternatively, you can use heading format:

```markdown
# Chat Session

## User:
Hello, how are you?

## Assistant:
I'm doing well, thank you for asking!
```

### Upload Process

1. From the home page, click the "Choose File" button
2. Select a JSON or Markdown file from your computer
3. Click the "Upload" button
4. Wait for the file to be processed (this may take a few moments for large files)
5. You will be redirected to the chat view page if the upload is successful

## Searching Chats

### Basic Search

1. Use the search bar at the top of any page
2. Enter your search query (e.g., "renewable energy")
3. Press Enter or click the search icon
4. View the search results, which will show matching messages from your chats

### Advanced Search

You can refine your search by:

- **Searching within a specific chat**: When viewing a chat, use the search bar to search only within that chat
- **Using quotes for exact phrases**: Enclose phrases in quotes (e.g., "solar panels") to search for exact matches
- **Using natural language queries**: The search uses semantic search, so you can use natural language (e.g., "discussions about climate change")

### Understanding Search Results

Search results show:
- The chat ID where the match was found
- The matching message with the search terms highlighted
- The role (user or assistant) who sent the message
- A relevance score indicating how well the message matches your query

Click on any result to view the full context of the conversation.

## Viewing Chats

### Chat View Interface

The chat view page shows:
- The chat ID and original filename
- The full conversation in chronological order
- Options to generate summaries and view the knowledge graph
- A search bar to search within this chat

### Navigating Long Conversations

For long conversations:
- Use your browser's search function (Ctrl+F or Cmd+F) to find specific text
- Use the browser's scrolling functionality to navigate through the conversation
- Consider generating a summary to get an overview of the conversation

## Generating Summaries

### Summary Types

The application supports two types of summaries:

- **Gist**: A brief overview of the entire conversation
- **Key Points**: A bullet-point list of the main topics and information

### Generating a Summary

1. Navigate to a specific chat by clicking on its ID from the home page
2. Click the "Generate Summary" button
3. Select the summary type from the dropdown menu
4. Click "Generate"
5. View the generated summary in the modal window

### Using Summaries

Summaries are useful for:
- Getting a quick overview of a conversation without reading the entire chat
- Identifying the main topics discussed
- Sharing the key points with others

## Exploring Knowledge Graphs

### Understanding Knowledge Graphs

Knowledge graphs visualize the entities (people, organizations, concepts, etc.) mentioned in the chat and the relationships between them.

### Viewing the Knowledge Graph

1. Navigate to a specific chat by clicking on its ID from the home page
2. Click the "View Knowledge Graph" button
3. The knowledge graph will be displayed as an interactive visualization

### Interacting with the Graph

You can interact with the graph in several ways:
- **Zoom**: Use the mouse wheel or pinch gesture to zoom in and out
- **Pan**: Click and drag to move around the graph
- **Select**: Click on a node to highlight its connections
- **Hover**: Hover over a node to see more details about the entity
- **Rearrange**: Drag nodes to rearrange the layout

### Interpreting the Graph

- **Nodes**: Represent entities mentioned in the chat
- **Node Colors**: Indicate the type of entity (person, organization, location, concept, etc.)
- **Edges**: Represent relationships between entities
- **Edge Labels**: Describe the type of relationship

## Troubleshooting

### Common Issues

#### Upload Errors

- **"Invalid file type"**: Ensure you're uploading a JSON or Markdown file with the correct extension
- **"Error processing file"**: Check that your file follows the correct format (see [Supported File Formats](#supported-file-formats))
- **"File too large"**: The maximum file size is 16MB; try splitting larger files

#### Search Issues

- **No results found**: Try using different search terms or check if the content is properly indexed
- **Irrelevant results**: Use more specific search terms or try using quotes for exact phrases

#### Summary Generation Errors

- **"Error generating summary"**: This may occur if the Gemini API key is not set or if there's an issue with the API
- **Timeout**: For very large chats, summary generation may time out; try again or use a smaller chat

#### Knowledge Graph Issues

- **Empty graph**: If no entities are detected in the chat, the graph will be empty
- **Browser performance**: Large graphs may slow down your browser; try using a more powerful device

### Getting Help

If you encounter issues not covered here:
1. Check the console logs for error messages
2. Refer to the [API Documentation](../API.md) for more details on the application's functionality
3. Submit an issue on the project's GitHub repository
