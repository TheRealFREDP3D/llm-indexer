#!/bin/bash

# Start the ChromaDB server in the background
echo "Starting ChromaDB server..."
python run_chroma_server.py &
CHROMA_PID=$!

# Wait for the ChromaDB server to start
echo "Waiting for ChromaDB server to start..."
sleep 5

# Start the Flask application
echo "Starting Flask application..."
python run.py

# When the Flask application exits, kill the ChromaDB server
echo "Shutting down ChromaDB server..."
kill $CHROMA_PID
