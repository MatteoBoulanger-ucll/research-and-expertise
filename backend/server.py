from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import subprocess

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
async def generate(request: Request):
    request_data = await request.json()
    user_input = request_data.get("prompt")

    if not user_input:
        raise HTTPException(status_code=400, detail="Missing 'prompt' in request body")

    # Run the Python script with the user-provided input
    result = subprocess.run(
        ["python", r"C:\Users\matte\Desktop\standalonetest\websockets_api.py", user_input],
        capture_output=True,
        text=True
    )

    # Return the output of the script
    return {"output": result.stdout}
