import os

# Specify file paths for text and images
text_files = {
    "header_text": "path/to/header_text.txt",
    "about_text": "path/to/about_text.txt",
    "footer_text": "path/to/footer_text.txt"
}

image_mapping = {
    "header_image": "path/to/header_image.jpg",
    "about_image": "path/to/about_image.png",
    "gallery_images": [
        "path/to/gallery_image1.jpg",
        "path/to/gallery_image2.jpg",
        "path/to/gallery_image3.jpg"
    ]
}

# Validate that text files exist
for key, path in text_files.items():
    if not os.path.exists(path):
        print(f"Text file not found: {path}")
        exit()

# Read content from text files
text_content = {key: open(path, "r").read().strip() for key, path in text_files.items()}

# Validate that the images exist
for key, value in image_mapping.items():
    if isinstance(value, list):
        image_mapping[key] = [img for img in value if os.path.exists(img)]
    elif os.path.exists(value):
        continue
    else:
        print(f"File not found: {value}")
        exit()

# HTML template with placeholders for text and images
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dynamic Website</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f9;
            color: #333;
        }
        header {
            background-color: #007BFF;
            color: white;
            padding: 20px;
            text-align: center;
        }
        header img {
            max-width: 100%;
            height: auto;
            border-radius: 10px;
        }
        main {
            padding: 20px;
            max-width: 800px;
            margin: auto;
        }
        .about-section img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px 0;
        }
        .image-gallery {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
        }
        .image-gallery img {
            max-width: 100%;
            height: auto;
            border: 2px solid #ccc;
            border-radius: 5px;
        }
        footer {
            background-color: #333;
            color: white;
            text-align: center;
            padding: 10px 0;
            position: fixed;
            bottom: 0;
            width: 100%;
        }
    </style>
</head>
<body>
    <header>
        <h1>{header_text}</h1>
        {header_image}
    </header>
    <main>
        <section class="about-section">
            <h2>About Me</h2>
            <p>{about_text}</p>
            {about_image}
        </section>
        <section class="image-gallery">
            <h2>Gallery</h2>
            {gallery_images}
        </section>
    </main>
    <footer>
        <p>{footer_text}</p>
    </footer>
</body>
</html>
"""

# Generate specific <img> tags for images
header_image_tag = f'<img src="{os.path.basename(image_mapping["header_image"])}" alt="Header Image">' if "header_image" in image_mapping else ""
about_image_tag = f'<img src="{os.path.basename(image_mapping["about_image"])}" alt="About Image">' if "about_image" in image_mapping else ""
gallery_image_tags = "\n".join([f'<img src="{os.path.basename(img)}" alt="Gallery Image">' for img in image_mapping["gallery_images"]]) if "gallery_images" in image_mapping else ""

# Replace placeholders in the HTML template with text and image data
html_content = html_content.format(
    header_text=text_content["header_text"],
    about_text=text_content["about_text"],
    footer_text=text_content["footer_text"],
    header_image=header_image_tag,
    about_image=about_image_tag,
    gallery_images=gallery_image_tags
)

# Save images and HTML file to an output directory
output_dir = "dynamic_website"
os.makedirs(output_dir, exist_ok=True)

# Copy images to the output directory
all_images = [image_mapping["header_image"], image_mapping["about_image"]] + image_mapping["gallery_images"]
for img in all_images:
    os.system(f'cp "{img}" "{output_dir}"')

# Save the HTML file
file_name = os.path.join(output_dir, "index.html")
with open(file_name, "w") as file:
    file.write(html_content)

print(f"Dynamic website generated successfully! Open {file_name} in your browser.")
