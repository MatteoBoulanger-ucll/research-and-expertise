from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import subprocess
from pydantic import BaseModel

# Create a Pydantic model for the request body
class GenerateRequest(BaseModel):
    text_prompt: str  # Define a field for the text prompt

app = FastAPI()

# Add CORS middleware to allow requests from specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # You can use "*" to allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.post("/generate")
async def generate(request: GenerateRequest):  # Accept the request with the text prompt
    # Get the text prompt from the request body
    text_prompt = request.text_prompt
    
    # Pass the text_prompt to your backend script
    result = subprocess.run(
        ["python", r"websockets_api.py", text_prompt],  # Pass the text prompt as an argument
        capture_output=True,
        text=True
    )

    # Return the output of the script
    return {"output": result.stdout}