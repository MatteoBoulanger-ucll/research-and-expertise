import os
import json

# Paths
OUTPUT_FOLDER = r"C:\Users\Jornick\Documents\comf\ComfyUI_windows_portable\ComfyUI\output\Research"
HTML_OUTPUT_PATH = os.path.join(OUTPUT_FOLDER, "generated_microsite.html")

# The new data file that has images, texts, selected_hex
SELECTED_DATA_PATH = os.path.join(OUTPUT_FOLDER, "selected_data.json")

# The text folder where the user-chosen .txt files live
TEXT_FOLDER = os.path.join(OUTPUT_FOLDER, "text")

# (Optional) Old fallback for images only, if needed
OLD_SELECTED_IMAGES_PATH = os.path.join(OUTPUT_FOLDER, "selected_images.json")

def read_text_file(file_path: str) -> str:
    """
    Safely read text from a file, returning 'misgenerated' if missing or empty.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            return content if content else "misgenerated"
    except FileNotFoundError:
        return "misgenerated"

def load_selected_data():
    """
    Attempts to load 'selected_data.json' with structure:
      {
        "images": { "Banner": "...", ... },
        "texts":  { "Header": "...", "Products": "...", ... },
        "selected_hex": ["#a26350", "#9d7986", ...]  // array of lines from a chunk in Hex_0001.txt
      }
    Falls back to old images file if needed (for backward compatibility).
    Returns (chosen_images, chosen_texts, chosen_hex_lines).
    """
    chosen_images = {}
    chosen_texts = {}
    chosen_hex = []  # an array of lines (each a hex like '#a26350')

    if os.path.exists(SELECTED_DATA_PATH):
        with open(SELECTED_DATA_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        chosen_images = data.get("images", {})
        chosen_texts = data.get("texts", {})
        chosen_hex = data.get("selected_hex", [])
    else:
        # If user never used new Editor, fallback to old selected_images.json
        if os.path.exists(OLD_SELECTED_IMAGES_PATH):
            with open(OLD_SELECTED_IMAGES_PATH, 'r', encoding='utf-8') as f:
                chosen_images = json.load(f)
        # No text picks => empty
        # No hex picks => empty

    return chosen_images, chosen_texts, chosen_hex

def get_image_path(chosen_images: dict, folder_name: str) -> str:
    """
    Return file:///-style path for the chosen image in `folder_name`, or 'misgenerated'.
    Example: chosen_images.get('Banner') => 'banner1.png'
    """
    image_name = chosen_images.get(folder_name, "misgenerated")
    if image_name == "misgenerated":
        return "misgenerated"

    folder_path = os.path.join(OUTPUT_FOLDER, "Pictures", folder_name)
    image_path = os.path.join(folder_path, image_name)
    if os.path.exists(image_path):
        # Convert backslashes -> forward slashes, prepend file:///
        return "file:///" + image_path.replace("\\", "/")
    else:
        return "misgenerated"

def read_chosen_text(chosen_texts: dict, prefix: str) -> (str, str):
    """
    If user chose e.g. 'Products': 'Products0002.txt',
    read that file, return (content, filename).
    If not found, return ('misgenerated','misgenerated').
    """
    filename = chosen_texts.get(prefix, "misgenerated")
    if filename == "misgenerated":
        return "misgenerated", "misgenerated"

    file_path = os.path.join(TEXT_FOLDER, filename)
    if os.path.exists(file_path):
        content = read_text_file(file_path)
        return content, filename
    else:
        return "misgenerated", "misgenerated"

def parse_hex_lines(chosen_hex: list) -> dict:
    """
    Interpret the chosen hex lines (like 8 lines from one chunk).
    We need 6 lines for:
      background, text, header, header_text, footer, footer_text
    If we have fewer than 6, fallback to defaults.
    If we have more, the first 6 are used, ignoring extra lines.
    """
    default_colors = {
        "background": "#f4f4f4",
        "text": "#333",
        "header": "#007BFF",
        "header_text": "#ffffff",
        "footer": "#333",
        "footer_text": "#ffffff"
    }

    if len(chosen_hex) < 6:
        return default_colors

    return {
        "background": chosen_hex[0].strip(),
        "text":       chosen_hex[1].strip(),
        "header":     chosen_hex[2].strip(),
        "header_text": chosen_hex[3].strip(),
        "footer":     chosen_hex[4].strip(),
        "footer_text": chosen_hex[5].strip()
    }

def generate_html() -> str:
    # 1. Load user picks (images, texts, and chosen hex lines)
    chosen_images, chosen_texts, chosen_hex = load_selected_data()

    # 2. Parse the chosen hex lines into color keys
    colors = parse_hex_lines(chosen_hex)

    # 3. For each text prefix, read the content & file name
    header_content, header_file = read_chosen_text(chosen_texts, "Header")
    products_content, products_file = read_chosen_text(chosen_texts, "Products")
    promo_content, promo_file = read_chosen_text(chosen_texts, "Promo")
    recap_content, recap_file = read_chosen_text(chosen_texts, "Recap")
    # ... add more if you have other text sections (Hex, etc.), 
    # though 'Hex' is used differently here.

    # 4. For images, get their file:// path
    banner_path = get_image_path(chosen_images, "Banner")
    logo_path   = get_image_path(chosen_images, "Logo")
    pallete_path = get_image_path(chosen_images, "Pallete")

    rndm_images = [
        get_image_path(chosen_images, "Rndm"),
        get_image_path(chosen_images, "Rndm2"),
        get_image_path(chosen_images, "Rndm3"),
        get_image_path(chosen_images, "Rndm4")
    ]
    rndm_images = [img for img in rndm_images if img != "misgenerated"]

    # 5. Build HTML with text-editing script
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
    <!-- HEADER -->
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
            {f"<img src='{pallete_path}' alt='Pallete' style='max-width:300px; display:block; margin-top:10px;' />"
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
        {f"<section><h2>Gallery</h2><div class='gallery'>" + 
           "".join(f"<img src='{img}' alt='Random'>" for img in rndm_images) + 
           "</div></section>" 
         if rndm_images else ""}
    </main>

    <footer>&copy; 2024 Generated Microsite</footer>
</body>
</html>
"""
    return html_output

if __name__ == "__main__":
    # Generate and write the HTML file
    final_html = generate_html()
    with open(HTML_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(final_html)
    print(f"Generated microsite saved at {HTML_OUTPUT_PATH}")
