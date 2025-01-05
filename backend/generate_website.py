import os
import json

# Paths
OUTPUT_FOLDER = r"C:\Users\Jornick\Documents\comf\ComfyUI_windows_portable\ComfyUI\output\Research"
HTML_OUTPUT_PATH = os.path.join(OUTPUT_FOLDER, "generated_microsite.html")

# Primary new JSON file with "images" and "texts"
SELECTED_DATA_PATH = os.path.join(OUTPUT_FOLDER, "selected_data.json")

# (Optional) Old images JSON for fallback
OLD_SELECTED_IMAGES_PATH = os.path.join(OUTPUT_FOLDER, "selected_images.json")

# The folder where .txt files are stored
TEXT_FOLDER = os.path.join(OUTPUT_FOLDER, "text")


def read_text_file(filepath: str) -> str:
    """Safely read a text file or return 'misgenerated' on error."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            return content if content else "misgenerated"
    except FileNotFoundError:
        return "misgenerated"


def load_selected_data():
    """
    Load the new 'selected_data.json' with structure:
    {
      "images": { "Banner": "...", "Logo": "...", ... },
      "texts": { "Header": "...", "Hex": "...", "Products": "...", "Promo": "...", "Recap": "..." }
    }
    For backward compatibility, if it doesn't exist, try old selected_images.json for images.
    """
    chosen_images = {}
    chosen_texts = {}

    if os.path.exists(SELECTED_DATA_PATH):
        with open(SELECTED_DATA_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        chosen_images = data.get("images", {})
        chosen_texts = data.get("texts", {})
    else:
        # Fallback to old selected_images.json (only images)
        if os.path.exists(OLD_SELECTED_IMAGES_PATH):
            with open(OLD_SELECTED_IMAGES_PATH, 'r', encoding='utf-8') as f:
                chosen_images = json.load(f)
        # No text picks => empty
        chosen_texts = {}

    return chosen_images, chosen_texts


def get_image_path(chosen_images: dict, folder_name: str) -> str:
    """
    Return file:/// path to the chosen image for `folder_name`, or "misgenerated" if not set.
    The images are stored in OUTPUT_FOLDER/Pictures/<folder_name>/<file>.
    """
    image_name = chosen_images.get(folder_name, "misgenerated")
    if image_name == "misgenerated":
        return "misgenerated"

    folder_path = os.path.join(OUTPUT_FOLDER, "Pictures", folder_name)
    image_path = os.path.join(folder_path, image_name)

    if os.path.exists(image_path):
        return "file:///" + image_path.replace("\\", "/")
    else:
        return "misgenerated"


def read_chosen_text(chosen_texts: dict, prefix: str) -> (str, str):
    """
    If user chose e.g. 'Header': 'Header_0002.txt', 
    then read that file and return (content, filename).
    If not chosen or not found, return ("misgenerated", "misgenerated").
    """
    filename = chosen_texts.get(prefix, "misgenerated")
    if filename == "misgenerated":
        return "misgenerated", "misgenerated"

    file_path = os.path.join(TEXT_FOLDER, filename)
    if os.path.exists(file_path):
        content = read_text_file(file_path)
        return (content, filename)
    else:
        return "misgenerated", "misgenerated"


def get_colors(chosen_texts: dict) -> dict:
    """
    If user picked a 'Hex' file in chosen_texts, use that for colors.
    Otherwise default. If the file is missing or 'misgenerated', fallback to default.
    """
    default_colors = {
        "background": "#f4f4f4",
        "text": "#333",
        "header": "#007BFF",
        "header_text": "#ffffff",
        "footer": "#333",
        "footer_text": "#ffffff"
    }

    # Load the chosen "Hex" file content (if any).
    hex_content, _ = read_chosen_text(chosen_texts, "Hex")
    if hex_content == "misgenerated":
        return default_colors

    lines = hex_content.splitlines()
    if len(lines) < 6:
        return default_colors

    return {
        "background": lines[0].strip(),
        "text":       lines[1].strip(),
        "header":     lines[2].strip(),
        "header_text": lines[3].strip(),
        "footer":     lines[4].strip(),
        "footer_text": lines[5].strip()
    }


def generate_html() -> str:
    # 1) Load user picks
    chosen_images, chosen_texts = load_selected_data()

    # 2) Colors from chosen "Hex"
    colors = get_colors(chosen_texts)

    # 3) Read text for each known prefix
    header_content, header_file = read_chosen_text(chosen_texts, "Header")
    products_content, products_file = read_chosen_text(chosen_texts, "Products")
    promo_content, promo_file = read_chosen_text(chosen_texts, "Promo")
    recap_content, recap_file = read_chosen_text(chosen_texts, "Recap")
    # If you have other prefixes, read them similarly

    # 4) Get image paths for each folder
    banner_path = get_image_path(chosen_images, "Banner")
    logo_path   = get_image_path(chosen_images, "Logo")
    pallete_path = get_image_path(chosen_images, "Pallete")

    rndm_images = [
        get_image_path(chosen_images, "Rndm"),
        get_image_path(chosen_images, "Rndm2"),
        get_image_path(chosen_images, "Rndm3"),
        get_image_path(chosen_images, "Rndm4")
    ]
    # Filter out any "misgenerated"
    rndm_images = [img for img in rndm_images if img != "misgenerated"]

    # 5) Build the HTML (similar to your old code, but dynamically referencing chosen file names)
    html_output = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
    <title>Generated Microsite</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: {colors['background']};
            color: {colors['text']};
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }}
        header {{
            background-color: {colors['header']};
            color: {colors['header_text']};
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        header img {{
            height: 50px;
            margin-right: 10px;
        }}
        main {{
            flex: 1;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        section {{
            margin-bottom: 20px;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        .edit-button {{
            margin-bottom: 10px;
            padding: 5px 10px;
            background-color: {colors['header']};
            color: {colors['header_text']};
            border: none;
            border-radius: 3px;
            cursor: pointer;
        }}
        footer {{
            background-color: {colors['footer']};
            color: {colors['footer_text']};
            text-align: center;
            padding: 10px 0;
        }}
        /* Simple gallery style for random images */
        .gallery {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .gallery img {{
            max-width: 200px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }}
    </style>
    <script>
        async function toggleEdit(button, textId, fileName) {{
            const textElement = document.getElementById(textId);
            const isEditable = textElement.contentEditable === "true";

            if (isEditable) {{
                // We are about to SAVE
                const content = textElement.innerText;
                try {{
                    const formData = new FormData();
                    formData.append("file_name", fileName);
                    formData.append("content", content);
                    const response = await fetch("http://127.0.0.1:8000/update-text", {{
                        method: "POST",
                        body: formData,
                    }});
                    if (response.ok) {{
                        alert("Text updated successfully!");
                        // Reload to re-generate the microsite with new text
                        location.reload(true);
                    }} else {{
                        const error = await response.json();
                        alert("Error saving: " + error.detail);
                    }}
                }} catch (error) {{
                    alert("Error saving: " + error.message);
                }}
            }}

            // Toggle contentEditable
            textElement.contentEditable = !isEditable;
            // Toggle button text
            button.innerText = isEditable ? "Edit" : "Save"; 
        }}
    </script>
</head>
<body>
    <header>
        {"<img src='" + logo_path + "' alt='Logo'>" if logo_path != "misgenerated" else ""}
        <h1 id="header-text">{header_content}</h1>
        {"<button class='edit-button' onclick=\"toggleEdit(this, 'header-text', '" + header_file + "')\">Edit</button>" 
            if header_file != "misgenerated" else ""}
    </header>

    <main>
        <!-- BANNER SECTION -->
        <section id="banner-section">
            {f"<img src='{banner_path}' alt='Banner' style='width: 100%; max-height: 300px;' />" 
                if banner_path != "misgenerated" else ""}
        </section>

        <!-- PRODUCTS -->
        <section id="products">
            {"<button class='edit-button' onclick=\"toggleEdit(this, 'products-text', '" + products_file + "')\">Edit</button>"
                if products_file != "misgenerated" else ""}
            <h2>Products</h2>
            <p id="products-text">{products_content}</p>
            {f"<img src='{pallete_path}' alt='Pallete' style='max-width:300px; display:block; margin-top:10px;'/>"
                if pallete_path != "misgenerated" else ""}
        </section>

        <!-- PROMO -->
        <section id="promo">
            {"<button class='edit-button' onclick=\"toggleEdit(this, 'promo-text', '" + promo_file + "')\">Edit</button>"
                if promo_file != "misgenerated" else ""}
            <h2>Promo</h2>
            <p id="promo-text">{promo_content}</p>
        </section>

        <!-- RECAP -->
        <section id="recap">
            {"<button class='edit-button' onclick=\"toggleEdit(this, 'recap-text', '" + recap_file + "')\">Edit</button>"
                if recap_file != "misgenerated" else ""}
            <h2>Recap</h2>
            <p id="recap-text">{recap_content}</p>
        </section>

        <!-- RANDOM IMAGE GALLERY -->
        {f"<section><h2>Gallery</h2><div class='gallery'>" + "".join(
            f"<img src='{img}' alt='Random'>" for img in rndm_images) + "</div></section>"
            if rndm_images else ""}
    </main>

    <footer>&copy; 2024 Generated Microsite</footer>
</body>
</html>"""
    return html_output


if __name__ == "__main__":
    html_output = generate_html()
    with open(HTML_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(html_output)
    print(f"Generated microsite saved at {HTML_OUTPUT_PATH}")
