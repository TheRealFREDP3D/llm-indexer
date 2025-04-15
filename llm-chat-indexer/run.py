import os
import uuid
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename

# Import configuration
from config.settings import VECTOR_STORE_PATH, KG_PATH

# Import modules
from src.parsing import JSONParser, MarkdownParser
from src.indexing import index_chat, get_collection_names
from src.search import search, search_all_collections
from src.summarization import generate_summary
from src.knowledge_graph import build_graph, save_graph, export_graph_for_vis

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # For flash messages

# Add template context processor to provide current year
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'raw_chats')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'json', 'md', 'txt'}


def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Homepage - Display indexed chats and upload form."""
    # Get list of indexed chats
    try:
        collections = get_collection_names()
        # Extract chat IDs from collection names (remove 'chat_' prefix)
        chat_ids = [coll[5:] for coll in collections if coll.startswith('chat_')]
    except Exception as e:
        chat_ids = []
        flash(f"Error loading indexed chats: {str(e)}", "error")

    return render_template('index.html', chat_ids=chat_ids)


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and indexing."""
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        # Generate a unique ID for the chat
        chat_id = str(uuid.uuid4())

        # Save the file
        if file.filename:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{chat_id}_{filename}")
            file.save(file_path)
        else:
            flash('Invalid filename', 'error')
            return redirect(url_for('index'))

        try:
            # Read the file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse the content based on file extension
            if filename.endswith('.json'):
                parser = JSONParser()
            elif filename.endswith('.md'):
                parser = MarkdownParser()
            else:  # Default to markdown for .txt
                parser = MarkdownParser()

            # Parse the content
            chat_data = parser.parse(content)

            # Index the chat
            index_chat(chat_data, chat_id)

            # Build and save knowledge graph
            build_graph(chat_data, chat_id)
            save_graph(chat_id)

            flash(f'File successfully uploaded and indexed with ID: {chat_id}', 'success')
            return redirect(url_for('view_chat', chat_id=chat_id))

        except Exception as e:
            flash(f'Error processing file: {str(e)}', 'error')
            return redirect(url_for('index'))

    flash('Invalid file type. Allowed types: json, md, txt', 'error')
    return redirect(url_for('index'))


@app.route('/search', methods=['GET'])
def search_chats():
    """Search indexed chats."""
    query = request.args.get('query', '')
    chat_id = request.args.get('chat_id', None)

    if not query:
        return render_template('search_results.html', results=None, query='')

    try:
        if chat_id:
            # Search in a specific chat
            results = {chat_id: search(query, chat_id)}
        else:
            # Search across all chats
            results = search_all_collections(query)

        return render_template('search_results.html', results=results, query=query)

    except Exception as e:
        flash(f'Error during search: {str(e)}', 'error')
        return render_template('search_results.html', results=None, query=query, error=str(e))


@app.route('/chat/<chat_id>')
def view_chat(chat_id):
    """View a specific chat with options for summaries and knowledge graph."""
    try:
        # Get the chat data (this would need to be implemented)
        # For now, we'll just show the chat ID and provide summary/graph options
        return render_template('chat_view.html', chat_id=chat_id)

    except Exception as e:
        flash(f'Error loading chat: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/summary/<chat_id>', methods=['GET'])
def get_summary(chat_id):
    """Generate a summary for a chat."""
    summary_type = request.args.get('type', 'gist')

    try:
        # This would need to retrieve the chat data first
        # For now, we'll return a placeholder
        summary = f"Summary of chat {chat_id} ({summary_type})"
        return jsonify({'summary': summary})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/graph/<chat_id>')
def get_graph_data(chat_id):
    """Return graph data for visualization."""
    format_type = request.args.get('format', 'json')

    try:
        # Export the graph for visualization
        graph_data = export_graph_for_vis(chat_id, format=format_type)
        return jsonify(graph_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
