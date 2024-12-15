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
        return image_path.replace(os.sep, "/")  # Replace backslashes with forward slashes for HTML
    return "misgenerated"  # Return "misgenerated" if the image is not found

# Function to generate the HTML content
def generate_html():
    html_content = "<html>\n<head>\n<title>Generated Microsite</title>\n</head>\n<body>\n"
    html_content += "<h1>Generated Microsite</h1>\n"
    
    # Add text sections
    for text_file in text_files:
        text_path = os.path.join(output_folder, "text", text_file)
        text_content = read_text_file(text_path)
        html_content += f"<h2>{text_file.replace('_', ' ').replace('.txt', '')}</h2>\n"
        html_content += f"<p>{text_content}</p>\n"
    
    # Add image sections
    for folder_name in image_folders:
        image_path = get_image_path(folder_name)
        if image_path != "misgenerated":  # Only add image if the path is valid
            image_tag = f'<img src="file:///{image_path}" alt="{folder_name}" width="300" />'
            html_content += f"<h3>{folder_name}</h3>\n"
            html_content += f"<p>{image_tag}</p>\n"
        else:
            html_content += f"<h3>{folder_name}</h3>\n"
            html_content += f"<p>misgenerated</p>\n"
    
    html_content += "</body>\n</html>"
    return html_content

# Path to save the generated HTML file
html_output_path = os.path.join(output_folder, "generated_microsite.html")

# Generate the HTML content and save it
html_content = generate_html()

with open(html_output_path, 'w') as file:
    file.write(html_content)

print(f"Generated HTML file saved at: {html_output_path}")
