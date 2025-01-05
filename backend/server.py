import re
from fastapi import FastAPI, HTTPException, File, Query, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import subprocess
import tempfile
import os
import json

app = FastAPI()

# ----- CORS MIDDLEWARE -----
# Allows your local file:// HTML to call http://127.0.0.1:8000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # For local dev, this is easiest. Consider restricting in prod.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# The directory containing your images
IMAGES_DIR = r"C:\Users\Jornick\Documents\comf\ComfyUI_windows_portable\ComfyUI\output\Research\Pictures"

# Mount the static files directory
app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")

OUTPUT_BASE_PATH = r"C:\Users\Jornick\Documents\comf\ComfyUI_windows_portable\ComfyUI\output\Research"
PICTURES_PATH = os.path.join(OUTPUT_BASE_PATH, "Pictures")

IMAGE_FOLDERS = [
    "Banner", "Logo", "Pallete", "Rndm", "Rndm2", "Rndm3", "Rndm4"
]

@app.post("/generate")
async def generate(
    text_prompt: str = Form(...),
    image: UploadFile = File(...)
):
    # Example endpoint to run websockets_api.py
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
    """Return a dict of folder -> [image file names]."""
    images_data = {}
    for folder in IMAGE_FOLDERS:
        folder_path = os.path.join(PICTURES_PATH, folder)
        if os.path.exists(folder_path):
            files = [
                f for f in os.listdir(folder_path)
                if f.lower().endswith('.png') or f.lower().endswith('.jpg') or f.lower().endswith('.jpeg')
            ]
            images_data[folder] = files
        else:
            images_data[folder] = []
    return images_data

@app.post("/finalize")
async def finalize(final_data: dict):
    """
    final_data structure:
    {
      "images": { "Banner": "banner.png", ... },
      "texts":  { "Header": "Header_0002.txt", "Promo": "Promo_0003.txt", ... }
    }
    """
    images = final_data.get("images", {})
    texts  = final_data.get("texts", {})

    # Save them all in one JSON file (or do separately if you prefer).
    # Example: store at "selected_data.json"
    selection_path = os.path.join(OUTPUT_BASE_PATH, "selected_data.json")
    with open(selection_path, "w", encoding="utf-8") as f:
        json.dump({"images": images, "texts": texts}, f, ensure_ascii=False, indent=4)

    # If your generate_website.py still expects "selected_images.json" for images:
    #   replicate just the images portion as well:
    old_selection_path = os.path.join(OUTPUT_BASE_PATH, "selected_images.json")
    with open(old_selection_path, "w", encoding="utf-8") as f:
        json.dump(images, f, ensure_ascii=False, indent=4)

    # Now run generate_website.py so the microsite is built
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
        "message": "Final microsite generated with your chosen images and text."
    }


@app.post("/update-text")
async def update_text(file_name: str = Form(...), content: str = Form(...)):
    """
    Updates the .txt file content, then regenerates the HTML to reflect changes.
    """
    text_folder = os.path.join(OUTPUT_BASE_PATH, "text")
    file_path = os.path.join(text_folder, file_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")

    # Write updated content directly to the file
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Re-run generate_website.py so the updated text is embedded in the HTML
        generate_website_result = subprocess.run(
            ["python", "generate_website.py"],
            capture_output=True,
            text=True
        )
        if generate_website_result.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=f"Error running generate_website.py after text update: {generate_website_result.stderr}"
            )

        return {"message": "File updated successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating file: {str(e)}")

@app.get("/text-files")
def list_text_files():
    text_folder = os.path.join(OUTPUT_BASE_PATH, "text")
    if not os.path.exists(text_folder):
        return {}

    # Regex that matches e.g. "Products_0001.txt" or "Products0001.txt"
    # Capturing group(1) = "Products"
    # Capturing group(2) = "0001"
    pattern = re.compile(r"^([A-Za-z]+)_?(\d{4})\.txt$", re.IGNORECASE)

    all_texts = {}

    for fname in os.listdir(text_folder):
        if fname.lower().endswith(".txt"):
            match = pattern.match(fname)
            if match:
                # e.g. "Products_0001.txt" => group(1)="Products", group(2)="0001"
                prefix = match.group(1)  # "Products"
            else:
                # Fallback: if it doesn't match e.g. "HexSomething.txt", or "Recap_abc.txt"
                # you can handle however you want. For now let's just remove extension
                # and use up to first underscore or entire name.
                name_no_ext = fname[:-4]  # remove ".txt"
                prefix = name_no_ext.split("_")[0]  # old fallback
            all_texts.setdefault(prefix, []).append(fname)

    return all_texts

@app.get("/text-content")
def get_text_content(file_name: str = Query(...)):
    """
    Returns the full text content of the given TXT file, if it exists in the text folder.
    Example request: GET /text-content?file_name=Header_0002.txt
    """
    text_folder = os.path.join(OUTPUT_BASE_PATH, "text")
    file_path = os.path.join(text_folder, file_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Text file {file_name} not found.")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return {"content": content}