import os
import json

# Path to the output folder where your content is stored
output_folder = r"C:\Users\Jornick\Documents\comf\ComfyUI_windows_portable\ComfyUI\output\Research"
selected_images_path = os.path.join(output_folder, "selected_images.json")

# Folders and text files to check
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

# Attempt to read chosen images from selected_images.json
chosen_images = {}
if os.path.exists(selected_images_path):
    with open(selected_images_path, 'r', encoding='utf-8') as f:
        chosen_images = json.load(f)
else:
    # If no file, default to misgenerated
    chosen_images = {folder: "misgenerated" for folder in image_folders}

def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            return content if content else "misgenerated"
    except FileNotFoundError:
        return "misgenerated"

def get_image_path(folder_name):
    folder_path = os.path.join(output_folder, "Pictures", folder_name)
    image_name = chosen_images.get(folder_name, "misgenerated")
    if image_name == "misgenerated":
        return "misgenerated"

    image_path = os.path.join(folder_path, image_name)

    if os.path.exists(image_path):
        return image_path.replace(os.sep, "/")
    return "misgenerated"

def get_colors():
    hex_file_path = os.path.join(output_folder, "text", "Hex_0001.txt")
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
        colors = {
            "background": lines[0].strip(),
            "text": lines[1].strip(),
            "header": lines[2].strip(),
            "header_text": lines[3].strip(),
            "footer": lines[4].strip(),
            "footer_text": lines[5].strip()
        }
        return colors
    except IndexError:
        return default_colors

def generate_html():
    colors = get_colors()

    # Text content
    text_contents = {}
    for txt in text_files:
        text_path = os.path.join(output_folder, "text", txt)
        text_contents[txt] = read_text_file(text_path)

    header_text = text_contents.get("Header_0001.txt", "misgenerated")
    products_text = text_contents.get("Products0001.txt", "misgenerated")
    promo_text = text_contents.get("Promo_0001.txt", "misgenerated")
    recap_text = text_contents.get("Recap_0001.txt", "misgenerated")

    banner_path = get_image_path("Banner")
    logo_path = get_image_path("Logo")
    pallete_path = get_image_path("Pallete")
    rndm_images = [
        get_image_path("Rndm"),
        get_image_path("Rndm2"),
        get_image_path("Rndm3"),
        get_image_path("Rndm4")
    ]
    rndm_images = [img for img in rndm_images if img != "misgenerated"]

    # Same improved HTML layout as previously given:
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Generated Microsite</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 0;
                background-color: {colors['background']};
                color: {colors['text']};
                display: flex;
                flex-direction: column;
                min-height: 100vh;
            }}
            header {{
                background: {colors['header']};
                color: {colors['header_text']};
                padding: 10px 20px;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }}
            header .logo {{
                display: flex;
                align-items: center;
            }}
            header .logo img {{
                height: 50px;
                margin-right: 10px;
            }}
            header h1 {{
                margin: 0;
                font-size: 1.8em;
            }}

            .hero {{
                position: relative;
                text-align: center;
                color: {colors['header_text']};
            }}
            .hero .banner-img {{
                width: 100%;
                max-height: 400px;
                object-fit: cover;
                display: block;
            }}
            .hero .hero-text {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(0,0,0,0.4);
                padding: 20px;
                border-radius: 5px;
            }}
            .hero .hero-text h2 {{
                margin: 0;
                font-size: 2.5em;
            }}

            main {{
                flex: 1;
                padding: 20px;
                max-width: 1200px;
                margin: 0 auto;
            }}
            section {{
                background: #fff;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                padding: 20px;
                margin-bottom: 20px;
            }}
            section h2 {{
                color: {colors['header']};
                margin-top: 0;
            }}
            .products-section {{
                display: flex;
                flex-wrap: wrap;
                align-items: center;
            }}
            .products-section .text {{
                flex: 1;
                min-width: 300px;
                margin-right: 20px;
            }}
            .products-section .image {{
                flex: 1;
                min-width: 300px;
            }}
            .products-section .image img {{
                max-width: 100%;
                height: auto;
                border-radius: 5px;
                border: 1px solid #ccc;
            }}

            .gallery {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
                gap: 10px;
            }}
            .gallery img {{
                width: 100%;
                height: auto;
                border-radius: 5px;
                border: 1px solid #ccc;
            }}

            footer {{
                text-align: center;
                padding: 10px;
                background: {colors['footer']};
                color: {colors['footer_text']};
            }}
        </style>
    </head>
    <body>
    """

    # HEADER
    html_content += "<header>"
    html_content += "<div class='logo'>"
    if logo_path != "misgenerated":
        html_content += f"<img src='file:///{logo_path}' alt='Logo' />"
    html_content += "<h1>Generated Microsite</h1>"
    html_content += "</div>"
    html_content += "</header>"

    # HERO SECTION (Banner + Header text)
    html_content += "<div class='hero'>"
    if banner_path != "misgenerated":
        html_content += f"<img src='file:///{banner_path}' alt='Banner' class='banner-img'/>"
    html_content += f"<div class='hero-text'><h2>{header_text}</h2></div>"
    html_content += "</div>"

    # MAIN CONTENT
    html_content += "<main>"

    # Products section with Pallete image if available
    html_content += "<section class='products-section'>"
    html_content += "<div class='text'>"
    html_content += "<h2>Products</h2>"
    html_content += f"<p>{products_text}</p>"
    html_content += "</div>"
    if pallete_path != "misgenerated":
        html_content += "<div class='image'>"
        html_content += f"<img src='file:///{pallete_path}' alt='Pallete' />"
        html_content += "</div>"
    html_content += "</section>"

    # Promo Section
    html_content += "<section>"
    html_content += "<h2>Promo</h2>"
    html_content += f"<p>{promo_text}</p>"
    html_content += "</section>"

    # Recap Section
    html_content += "<section>"
    html_content += "<h2>Recap</h2>"
    html_content += f"<p>{recap_text}</p>"
    html_content += "</section>"

    # Gallery of Rndm images
    if rndm_images:
        html_content += "<section>"
        html_content += "<h2>Gallery</h2>"
        html_content += "<div class='gallery'>"
        for img_path in rndm_images:
            html_content += f"<img src='file:///{img_path}' alt='Gallery Image'/>"
        html_content += "</div>"
        html_content += "</section>"

    html_content += "</main>"

    # FOOTER
    html_content += f"""
    <footer>
        <p>&copy; 2024 Generated Microsite. All Rights Reserved.</p>
    </footer>
    </body>
    </html>
    """
    return html_content

html_output_path = os.path.join(output_folder, "generated_microsite.html")
html_content = generate_html()
with open(html_output_path, 'w', encoding='utf-8') as file:
    file.write(html_content)

print(f"Generated HTML file saved at: {html_output_path}")
