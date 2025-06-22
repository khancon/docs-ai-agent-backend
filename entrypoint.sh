#!/bin/sh

# Start the server in background
ollama serve &

# Wait for server to be ready (you can add retries here)
sleep 5

# Now pull the model
ollama pull deepseek-llm

# Keep the server running in foreground
fg %1
