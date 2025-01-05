import os
import json

# Define paths
output_folder = r"C:\Users\Jornick\Documents\comf\ComfyUI_windows_portable\ComfyUI\output\Research"
selected_images_path = os.path.join(output_folder, "selected_images.json")

TEXT_FOLDER = os.path.join(output_folder, "text")
HTML_OUTPUT_PATH = os.path.join(output_folder, "generated_microsite.html")

text_files = [
    "Header_0001.txt",
    "Hex_0001.txt",
    "Products0001.txt",
    "Promo_0001.txt",
    "Recap_0001.txt"
]

image_folders = [
    "Banner", "Logo", "Pallete", "Rndm", "Rndm2", "Rndm3", "Rndm4"
]

# Load selected images
if os.path.exists(selected_images_path):
    with open(selected_images_path, 'r', encoding='utf-8') as f:
        chosen_images = json.load(f)
else:
    chosen_images = {folder: "misgenerated" for folder in image_folders}

def read_text_file(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            return content if content else "misgenerated"
    except FileNotFoundError:
        return "misgenerated"

def get_image_path(folder_name: str) -> str:
    folder_path = os.path.join(output_folder, "Pictures", folder_name)
    image_name = chosen_images.get(folder_name, "misgenerated")
    if image_name == "misgenerated":
        return "misgenerated"

    image_path = os.path.join(folder_path, image_name)
    if os.path.exists(image_path):
        # Convert Windows backslashes to forward slashes for file:///
        return image_path.replace("\\", "/")
    else:
        return "misgenerated"

def get_colors() -> dict:
    hex_file_path = os.path.join(TEXT_FOLDER, "Hex_0001.txt")
    hex_content = read_text_file(hex_file_path)

    default_colors = {
        "background": "#f4f4f4",
        "text": "#333",
        "header": "#007BFF",
        "header_text": "#ffffff",
        "footer": "#333",
        "footer_text": "#ffffff"
    }

    if hex_content == "misgenerated":
        return default_colors

    try:
        lines = hex_content.splitlines()
        return {
            "background": lines[0].strip(),
            "text":       lines[1].strip(),
            "header":     lines[2].strip(),
            "header_text": lines[3].strip(),
            "footer":     lines[4].strip(),
            "footer_text": lines[5].strip()
        }
    except IndexError:
        return default_colors

def generate_html() -> str:
    colors = get_colors()

    # Read text content
    text_contents = {txt: read_text_file(os.path.join(TEXT_FOLDER, txt)) for txt in text_files}

    # Image paths
    banner_path   = get_image_path("Banner")
    logo_path     = get_image_path("Logo")
    pallete_path  = get_image_path("Pallete")

    rndm_images = [
        get_image_path("Rndm"),
        get_image_path("Rndm2"),
        get_image_path("Rndm3"),
        get_image_path("Rndm4")
    ]
    rndm_images = [img for img in rndm_images if img != "misgenerated"]

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
                        // This reload will load the newly generated HTML with updated text
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
        {"<img src='file:///" + logo_path + "' alt='Logo'>" if logo_path != "misgenerated" else ""}
        <h1 id="header-text">{text_contents.get('Header_0001.txt', 'misgenerated')}</h1>
        <button class="edit-button" onclick="toggleEdit(this, 'header-text', 'Header_0001.txt')">Edit</button>
    </header>

    <main>
        <!-- BANNER SECTION -->
        <section id="banner-section">
            {"<img src='file:///" + banner_path + "' alt='Banner' style='width: 100%; max-height: 300px;' />" 
                if banner_path != "misgenerated" else ""}
        </section>

        <!-- PRODUCTS -->
        <section id="products">
            <button class="edit-button" onclick="toggleEdit(this, 'products-text', 'Products0001.txt')">Edit</button>
            <h2>Products</h2>
            <p id="products-text">{text_contents.get('Products0001.txt', 'misgenerated')}</p>
            {"<img src='file:///" + pallete_path + "' alt='Pallete' style='max-width:300px; display:block; margin-top:10px;'/>"
                if pallete_path != "misgenerated" else ""}
        </section>

        <!-- PROMO -->
        <section id="promo">
            <button class="edit-button" onclick="toggleEdit(this, 'promo-text', 'Promo_0001.txt')">Edit</button>
            <h2>Promo</h2>
            <p id="promo-text">{text_contents.get('Promo_0001.txt', 'misgenerated')}</p>
        </section>

        <!-- RECAP -->
        <section id="recap">
            <button class="edit-button" onclick="toggleEdit(this, 'recap-text', 'Recap_0001.txt')">Edit</button>
            <h2>Recap</h2>
            <p id="recap-text">{text_contents.get('Recap_0001.txt', 'misgenerated')}</p>
        </section>

        <!-- RANDOM IMAGE GALLERY -->
        {"<section><h2>Gallery</h2><div class='gallery'>" 
          + "".join(f"<img src='file:///{rndm}' alt='Random'>" for rndm in rndm_images) 
          + "</div></section>" 
            if rndm_images else ""}
    </main>

    <footer>&copy; 2024 Generated Microsite</footer>
</body>
</html>
"""
    return html_output

if __name__ == "__main__":
    # Generate the HTML file
    html_output = generate_html()
    with open(HTML_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(html_output)
    print(f"Generated microsite saved at {HTML_OUTPUT_PATH}")
