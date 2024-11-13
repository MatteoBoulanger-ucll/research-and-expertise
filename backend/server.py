from fastapi import FastAPI
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
async def generate():
    # Run the Python script without any arguments
    result = subprocess.run(
        ["python", r"C:\Users\matte\Desktop\standalonetest\websockets_api.py"],
        capture_output=True,
        text=True
    )

    # Return the output of the script
    return {"output": result.stdout}
