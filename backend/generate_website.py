import os

# Path to the output folder where your content is stored
output_folder = r"C:\Users\Jornick\Documents\comf\ComfyUI_windows_portable\ComfyUI\output\Research"

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

# Define image names for each folder
image_names = {
    "Banner": "Ban0001.png",
    "Logo": "Log0001.png",
    "Pallete": "Pal0001.png",
    "Rndm": "Rndm0001.png",
    "Rndm2": "Rndm0001.png",
    "Rndm3": "Rndm0001.png",
    "Rndm4": "Rndm0001.png",
}

# Function to read text files and return the content


def read_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read().strip()
            return content if content else "misgenerated"  # Return "misgenerated" if empty
    except FileNotFoundError:
        return "misgenerated"  # Return "misgenerated" if the file is not found


# Function to get the first image file path from a folder


def get_image_path(folder_name):
    folder_path = os.path.join(output_folder, "Pictures", folder_name)
    image_name = image_names.get(folder_name)
    image_path = os.path.join(folder_path, image_name)

    # Check if the image exists and return the path, else return an empty string
    if os.path.exists(image_path):
        # Replace backslashes with forward slashes for HTML
        return image_path.replace(os.sep, "/")
    return "misgenerated"  # Return "misgenerated" if the image is not found


# Function to extract colors from Hex_0001.txt


def get_colors():
    hex_file_path = os.path.join(output_folder, "text", "Hex_0001.txt")
    hex_content = read_text_file(hex_file_path)

    # Default colors if file is empty or missing
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


# Function to generate the HTML content


def generate_html():
    colors = get_colors()

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
                padding: 20px 10px;
                text-align: center;
            }}
            header h1 {{
                margin: 0;
                font-size: 2.5em;
            }}
            main {{
                flex: 1;
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                padding: 20px;
                background-color: {colors['background']};
            }}
            section {{
                background: #fff;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                padding: 20px;
            }}
            section h2 {{
                color: {colors['header']};
            }}
            .image-section img {{
                max-width: 100%;
                height: auto;
                margin-top: 10px;
                border-radius: 5px;
                border: 1px solid #ccc;
            }}
            footer {{
                text-align: center;
                padding: 10px;
                background: {colors['footer']};
                color: {colors['footer_text']};
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>Generated Microsite</h1>
        </header>
        <main>
    """

    # Add text sections
    for text_file in text_files:
        text_path = os.path.join(output_folder, "text", text_file)
        text_content = read_text_file(text_path)
        html_content += f"""
        <section>
            <h2>{text_file.replace('_', ' ').replace('.txt', '')}</h2>
            <p>{text_content}</p>
        </section>
        """

    # Add image sections
    for folder_name in image_folders:
        image_path = get_image_path(folder_name)
        if image_path != "misgenerated":  # Only add image if the path is valid
            html_content += f"""
            <section class="image-section">
                <h2>{folder_name}</h2>
                <img src="file:///{image_path}" alt="{folder_name}" />
            </section>
            """
        else:
            html_content += f"""
            <section>
                <h2>{folder_name}</h2>
                <p>misgenerated</p>
            </section>
            """

    # Add footer
    html_content += f"""
        </main>
        <footer>
            <p>&copy; 2024 Generated Microsite. All Rights Reserved.</p>
        </footer>
    </body>
    </html>
    """

    return html_content


# Path to save the generated HTML file
html_output_path = os.path.join(output_folder, "generated_microsite.html")

# Generate the HTML content and save it
html_content = generate_html()

with open(html_output_path, 'w') as file:
    file.write(html_content)

print(f"Generated HTML file saved at: {html_output_path}")
