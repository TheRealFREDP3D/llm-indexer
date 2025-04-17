# LLM Chat Indexer File Format Specification

This document provides detailed specifications for the file formats supported by the LLM Chat Indexer application.

## Supported File Formats

The LLM Chat Indexer supports the following file formats:
1. JSON
2. Markdown

## JSON Format

### Basic Structure

JSON files should contain a `messages` array with objects representing individual messages:

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

### Required Fields

Each message object must contain:

- `role`: The role of the message sender (string)
  - Valid values: `"user"`, `"assistant"`, `"system"`
- `content`: The content of the message (string)

### Optional Fields

Each message object may also contain:

- `timestamp`: The time the message was sent (string in ISO 8601 format)
- `id`: A unique identifier for the message (string)
- `metadata`: Additional metadata about the message (object)

### Alternative Structure

The application also supports a flat array of message objects:

```json
[
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
```

### Example

Here's a complete example of a valid JSON file:

```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant.",
      "timestamp": "2023-01-01T12:00:00Z"
    },
    {
      "role": "user",
      "content": "Hello, can you tell me about renewable energy?",
      "timestamp": "2023-01-01T12:00:10Z",
      "id": "msg_123",
      "metadata": {
        "user_id": "user_456",
        "client": "web"
      }
    },
    {
      "role": "assistant",
      "content": "Renewable energy comes from sources that naturally replenish, such as sunlight, wind, rain, tides, waves, and geothermal heat. Unlike fossil fuels, these energy sources won't run out and generally don't produce greenhouse gases.",
      "timestamp": "2023-01-01T12:00:20Z",
      "id": "msg_124",
      "metadata": {
        "model": "gemini-pro",
        "tokens": 42
      }
    }
  ]
}
```

## Markdown Format

### Basic Structure

Markdown files should use headers or bold text to indicate the role of each message:

#### Using Bold Text

```markdown
**User**: Hello, how are you?

**Assistant**: I'm doing well, thank you for asking!
```

#### Using Headers

```markdown
## User:
Hello, how are you?

## Assistant:
I'm doing well, thank you for asking!
```

### Required Elements

- Role indicator: Either bold text (`**User**:`) or header (`## User:`)
- Message content: The text following the role indicator

### Optional Elements

- Title: A top-level header (`# Chat Title`) at the beginning of the file
- Timestamps: Can be included in parentheses after the role indicator

### Supported Roles

- `User` or `Human`: Messages from the user
- `Assistant` or `AI`: Messages from the assistant
- `System`: System messages

### Example

Here's a complete example of a valid Markdown file:

```markdown
# Conversation about Renewable Energy

**System** (2023-01-01T12:00:00Z): You are a helpful assistant.

**User** (2023-01-01T12:00:10Z): Hello, can you tell me about renewable energy?

**Assistant** (2023-01-01T12:00:20Z): Renewable energy comes from sources that naturally replenish, such as sunlight, wind, rain, tides, waves, and geothermal heat. Unlike fossil fuels, these energy sources won't run out and generally don't produce greenhouse gases.

**User**: What are the main types of renewable energy?

**Assistant**: The main types of renewable energy are:

1. Solar energy: Harnessing power from the sun
2. Wind energy: Using wind to generate electricity
3. Hydroelectric energy: Using flowing water to generate electricity
4. Biomass energy: Using organic material to produce energy
5. Geothermal energy: Using heat from the Earth's core
```

## Parsing Process

### JSON Parsing

1. The file is read and parsed as JSON
2. If the JSON contains a `messages` array, that array is used
3. If the JSON is an array, it is used directly
4. Each message object is validated to ensure it has the required fields
5. Optional fields are preserved if present

### Markdown Parsing

1. The file is read as text
2. The text is split into lines
3. Lines are processed to identify role indicators and message content
4. Messages are grouped by role and content
5. The resulting messages are converted to the standardized format

## Standardized Message Format

Internally, all messages are converted to a standardized format:

```python
{
    "role": str,       # "user", "assistant", or "system"
    "content": str,    # The message content
    "timestamp": str,  # ISO 8601 timestamp (if available)
    "metadata": dict   # Additional metadata (if available)
}
```

## Error Handling

### JSON Parsing Errors

- Invalid JSON syntax: Returns an error
- Missing required fields: Returns an error
- Invalid role values: Defaults to "user" with a warning

### Markdown Parsing Errors

- Missing role indicators: Skips the content with a warning
- Ambiguous role indicators: Uses best guess with a warning
- Empty content: Skips the message with a warning

## Best Practices

### JSON Files

- Always include a `messages` array
- Always include `role` and `content` fields for each message
- Use ISO 8601 format for timestamps
- Include metadata when available

### Markdown Files

- Use consistent formatting for role indicators
- Include a title at the beginning of the file
- Separate messages with blank lines
- Use proper Markdown formatting for structured content

## Validation

You can validate your files before uploading:

- JSON files: Use a JSON validator and check against the schema
- Markdown files: Ensure proper formatting and role indicators

## Converting Between Formats

### JSON to Markdown

```python
import json

def json_to_markdown(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    messages = data.get('messages', data)
    markdown = "# Chat Conversation\n\n"
    
    for msg in messages:
        role = msg['role'].capitalize()
        content = msg['content']
        timestamp = msg.get('timestamp', '')
        
        if timestamp:
            markdown += f"**{role}** ({timestamp}): {content}\n\n"
        else:
            markdown += f"**{role}**: {content}\n\n"
    
    return markdown
```

### Markdown to JSON

```python
import re
import json
from datetime import datetime

def markdown_to_json(md_file):
    with open(md_file, 'r') as f:
        content = f.read()
    
    # Regular expression to match messages
    pattern = r'\*\*(User|Assistant|System)\*\*(?:\s+\((.*?)\))?\s*:\s*(.*?)(?=\n\n\*\*|\Z)'
    matches = re.findall(pattern, content, re.DOTALL)
    
    messages = []
    for role, timestamp, text in matches:
        message = {
            "role": role.lower(),
            "content": text.strip()
        }
        
        if timestamp:
            message["timestamp"] = timestamp
        
        messages.append(message)
    
    return {"messages": messages}
```
