from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import tempfile
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate(
    text_prompt: str = Form(...),
    image: UploadFile = File(...)
):
    # Save the uploaded file to a temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        image_path = os.path.join(tmpdir, image.filename)
        # Read and write the file content
        with open(image_path, "wb") as f:
            f.write(await image.read())

        # Run websockets_api.py with the text_prompt and image_path arguments
        websockets_result = subprocess.run(
            ["python", "websockets_api.py", text_prompt, image_path],
            capture_output=True,
            text=True
        )

        if websockets_result.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=f"Error running websockets_api.py: {websockets_result.stderr}"
            )

        # Run generate_website.py
        generate_website_result = subprocess.run(
            ["python", "generate_website.py"],
            capture_output=True,
            text=True
        )

        if generate_website_result.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=f"Error running generate_website.py: {generate_website_result.stderr}"
            )

        return {
            "websockets_output": websockets_result.stdout,
            "generate_website_output": generate_website_result.stdout
        }
