import logging
import os
import uuid
from datetime import datetime

# Import configuration
from config.config import config
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for

# Import Swagger documentation
from src.api.swagger import API_URL, SWAGGER_URL, swagger_spec, swagger_ui_blueprint
from src.indexing import get_collection_names, index_chat
from src.knowledge_graph import build_graph, export_graph_for_vis, save_graph

# Import modules
from src.parsing import JSONParser, MarkdownParser
from src.search import search, search_all_collections
from src.summarization import generate_summary
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # For flash messages

# Register Swagger UI blueprint
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Endpoint to serve the Swagger JSON specification
@app.route(API_URL)
def swagger_json():
    """Return the Swagger JSON specification."""
    return jsonify(swagger_spec)

# Add template context processor to provide current year
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
        # Get the chat data from the raw file
        chat_data = None
        file_path = None

        # Look for the chat file in the upload folder
        for filename in os.listdir(UPLOAD_FOLDER):
            if filename.startswith(chat_id):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Parse the content based on file extension
                if filename.endswith('.json'):
                    parser = JSONParser()
                elif filename.endswith('.md'):
                    parser = MarkdownParser()
                else:  # Default to markdown for .txt
                    parser = MarkdownParser()

                chat_data = parser.parse(content)
                break

        if not chat_data:
            flash('Chat data not found', 'error')
            return redirect(url_for('index'))

        # Get the original filename without the chat_id prefix
        original_filename = os.path.basename(file_path).replace(f"{chat_id}_", "") if file_path else ""

        return render_template('chat_view.html', chat_id=chat_id, chat_data=chat_data, filename=original_filename)

    except Exception as e:
        flash(f'Error loading chat: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/summary/<chat_id>', methods=['GET'])
def get_summary(chat_id):
    """Generate a summary for a chat."""
    summary_type = request.args.get('type', 'gist')

    try:
        # Get the chat data from the raw file
        # In a real implementation, you would retrieve this from a database
        chat_data = None

        # Look for the chat file in the upload folder
        for filename in os.listdir(UPLOAD_FOLDER):
            if filename.startswith(chat_id):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Parse the content based on file extension
                if filename.endswith('.json'):
                    parser = JSONParser()
                elif filename.endswith('.md'):
                    parser = MarkdownParser()
                else:  # Default to markdown for .txt
                    parser = MarkdownParser()

                chat_data = parser.parse(content)
                break

        if not chat_data:
            return jsonify({'error': 'Chat data not found'}), 404

        # Generate the summary
        summary = generate_summary(chat_data, summary_type)
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

    except FileNotFoundError as e:
        logger.warning(f"Knowledge graph not found for chat {chat_id}: {str(e)}")
        # Return an empty graph structure instead of an error
        if format_type == 'json':
            return jsonify({'nodes': [], 'links': []})
        elif format_type == 'cytoscape':
            return jsonify({'elements': []})
        else:
            return jsonify({'error': f'Unsupported format: {format_type}'}), 400

    except Exception as e:
        logger.error(f"Error retrieving graph data for chat {chat_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Validate configuration before starting the app
    try:
        # Log configuration values for debugging
        logger.info("Starting application with the following configuration:")
        logger.info(f"VECTOR_STORE_PATH: {config.VECTOR_STORE_PATH}")
        logger.info(f"KG_PATH: {config.KG_PATH}")
        logger.info(f"SENTENCE_TRANSFORMER_MODEL: {config.SENTENCE_TRANSFORMER_MODEL}")
        logger.info(f"API Documentation: http://localhost:5000{SWAGGER_URL}")

        # Check for required API keys
        if not config.GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY is not set. Summarization features will not work.")

        # Start the Flask app
        app.run(debug=True)
    except Exception as e:
        logger.error(f"Error starting application: {str(e)}")
        raise
