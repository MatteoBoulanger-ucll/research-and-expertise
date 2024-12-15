import os

# Path to the output folder where your content is stored
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # This gets the RESEARCH-AND-EXPERTISE directory
microsite_path = os.path.join(base_path, "microsite", "pages", "generated")  # Path to the microsite/pages/generated folder

# Ensure the microsite/pages/generated folder exists
os.makedirs(microsite_path, exist_ok=True)

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
    folder_path = os.path.join(base_path, "output", "Research", "Pictures", folder_name)
    image_name = image_names.get(folder_name)
    image_path = os.path.join(folder_path, image_name)
    
    # Check if the image exists and return the path, else return an empty string
    if os.path.exists(image_path):
        return image_path.replace(os.sep, "/")  # Replace backslashes with forward slashes for HTML
    return "misgenerated"  # Return "misgenerated" if the image is not found

# Function to generate the React component (TSX) content
def generate_react_tsx():
    # Initialize the TSX content as a React component with the Header import
    tsx_content = """
import React from 'react';
import Header from '../../components/header'; 

const GeneratedMicrosite: React.FC = () => {
    return (
        <div className="container mx-auto px-4 py-8">
            <Header />
            <h1 className="text-4xl font-bold text-center mb-8">Generated Microsite</h1>
    """

    # Add text sections
    for text_file in text_files:
        text_path = os.path.join(base_path, "output", "Research", "text", text_file)
        text_content = read_text_file(text_path)
        tsx_content += f"""
            <section className="mb-8">
                <h2 className="text-2xl font-semibold">{text_file.replace('_', ' ').replace('.txt', '')}</h2>
                <p className="text-lg">{text_content}</p>
            </section>
        """
    
    # Add image sections
    for folder_name in image_folders:
        image_path = get_image_path(folder_name)
        if image_path != "misgenerated":  # Only add image if the path is valid
            tsx_content += f"""
            <section className="mb-8">
                <h3 className="text-xl font-semibold">{folder_name}</h3>
                <img src="{image_path}" alt="{folder_name}" className="w-full h-auto" />
            </section>
            """
        else:
            tsx_content += f"""
            <section className="mb-8">
                <h3 className="text-xl font-semibold">{folder_name}</h3>
                <p>misgenerated</p>
            </section>
            """
    
    # Closing the div and React component
    tsx_content += """
        </div>
    );
};

export default GeneratedMicrosite;
"""

    return tsx_content

# Path to save the generated React component file (index.tsx)
tsx_output_path = os.path.join(microsite_path, "index.tsx")

# Generate the TSX content and save it
tsx_content = generate_react_tsx()

# Save the TSX file
with open(tsx_output_path, 'w') as file:
    file.write(tsx_content)

print(f"Generated TSX file saved at: {tsx_output_path}")
