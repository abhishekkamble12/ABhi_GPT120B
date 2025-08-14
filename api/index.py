from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
import subprocess
import os
from dotenv import load_dotenv

app = FastAPI()

# Load environment variables
load_dotenv()

# Serve the main page
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Kaggle Red-Teaming Assistant</title>
        </head>
        <body>
            <h1>Kaggle Red-Teaming Assistant</h1>
            <p>Use the API endpoint at /api/chat to interact with the assistant.</p>
        </body>
    </html>
    """

# API endpoint for chat
@app.post("/api/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    
    # Here you would add your actual model integration
    # For now, this is a placeholder response
    response = {
        "response": f"Received your message: {prompt}",
        "status": "success"
    }
    
    return response

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
