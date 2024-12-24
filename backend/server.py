from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import subprocess
import tempfile
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # or add 127.0.0.1 if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# The directory containing your images
IMAGES_DIR = r"C:\Users\Jornick\Documents\comf\ComfyUI_windows_portable\ComfyUI\output\Research\Pictures"

# Mount the static files directory
# After this, you can access images at http://127.0.0.1:8000/images/<FolderName>/<ImageName>.png
app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")

OUTPUT_BASE_PATH = r"C:\Users\Jornick\Documents\comf\ComfyUI_windows_portable\ComfyUI\output\Research"
PICTURES_PATH = os.path.join(OUTPUT_BASE_PATH, "Pictures")
# OUTPUT_BASE_PATH = r"C:\Users\matte\Desktop\output"

IMAGE_FOLDERS = [
    "Banner", "Logo", "Pallete", "Rndm", "Rndm2", "Rndm3", "Rndm4"
]

@app.post("/generate")
async def generate(
    text_prompt: str = Form(...),
    image: UploadFile = File(...)
):
    with tempfile.TemporaryDirectory() as tmpdir:
        image_path = os.path.join(tmpdir, image.filename)
        with open(image_path, "wb") as f:
            f.write(await image.read())

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

        return {
            "websockets_output": websockets_result.stdout,
            "message": "Images generated. Proceed to /select-images in frontend."
        }

@app.get("/images")
def list_images():
    images_data = {}
    for folder in IMAGE_FOLDERS:
        folder_path = os.path.join(PICTURES_PATH, folder)
        if os.path.exists(folder_path):
            files = [f for f in os.listdir(folder_path) if f.lower().endswith('.png')]
            images_data[folder] = files
        else:
            images_data[folder] = []
    return images_data

@app.post("/finalize")
async def finalize(selected_images: dict):
    selection_path = os.path.join(OUTPUT_BASE_PATH, "selected_images.json")
    with open(selection_path, "w", encoding="utf-8") as f:
        json.dump(selected_images, f, ensure_ascii=False, indent=4)

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
        "message": "Final microsite generated with your chosen images."
    }


@app.post("/update-text")
async def update_text(file_name: str = Form(...), content: str = Form(...)):
    text_folder = os.path.join(OUTPUT_BASE_PATH, "text")
    file_path = os.path.join(text_folder, file_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")

    # Write updated content directly to the file
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return {"message": "File updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating file: {str(e)}")

