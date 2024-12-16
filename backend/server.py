from fastapi import FastAPI, HTTPException
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

    # Step 1: Run the websockets_api.py script
    websockets_result = subprocess.run(
        ["python", "websockets_api.py", text_prompt],  # Pass the text prompt as an argument
        capture_output=True,
        text=True
    )

    # Check if websockets_api.py ran successfully
    if websockets_result.returncode != 0:
        raise HTTPException(
            status_code=500,
            detail=f"Error running websockets_api.py: {websockets_result.stderr}"
        )

    # Step 2: Run the generate_website.py script
    generate_website_result = subprocess.run(
        ["python", "generate_website.py"],  # Assuming no arguments are needed
        capture_output=True,
        text=True
    )

    # Check if generate_website.py ran successfully
    if generate_website_result.returncode != 0:
        raise HTTPException(
            status_code=500,
            detail=f"Error running generate_website.py: {generate_website_result.stderr}"
        )

    # Return the output of both scripts
    return {
        "websockets_output": websockets_result.stdout,
        "generate_website_output": generate_website_result.stdout
    }
