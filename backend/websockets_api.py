#This is an example that uses the websockets api to know when a prompt execution is done
#Once the prompt execution is done it downloads the images using the /history endpoint

import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
import urllib.request
import urllib.parse
from tkinter import Tk, filedialog, simpledialog  
import os
from PIL import Image
import io
import os
import shutil

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())


root = Tk()
root.withdraw()  
image_path = filedialog.askopenfilename(title="Selecteer een afbeelding", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])


def clear_output_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)  # Delete the folder and its contents
        os.makedirs(folder_path)  # Recreate an empty folder
        print(f"Cleared and recreated folder: {folder_path}")
    else:
        os.makedirs(folder_path)  # Create the folder if it doesn't exist
        print(f"Created folder: {folder_path}")

# Define your folder path
output_folder = "./output/index/"
clear_output_folder(output_folder)

# Controleer of de gebruiker een afbeelding heeft geselecteerd
if not image_path:
    print("Geen afbeelding geselecteerd. Script wordt beëindigd.")
    exit()


# text_prompt = simpledialog.askstring("Input", "Voer een tekstprompt in:")

text_prompt = "give me a webshop for 3D printers"

# Check if a text prompt was entered
if not text_prompt:
    print("Geen tekstprompt ingevoerd. Script wordt beëindigd.")
    exit()

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req =  urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()

def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())

def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break #Execution is done
        else:
            # If you want to be able to decode the binary stream for latent previews, here is how you can do it:
            # bytesIO = BytesIO(out[8:])
            # preview_image = Image.open(bytesIO) # This is your preview in PIL image format, store it in a global
            continue #previews are binary data

    history = get_history(prompt_id)[prompt_id]
    for node_id in history['outputs']:
        node_output = history['outputs'][node_id]
        images_output = []
        if 'images' in node_output:
            for image in node_output['images']:
                image_data = get_image(image['filename'], image['subfolder'], image['type'])
                images_output.append(image_data)
        output_images[node_id] = images_output

    return output_images

with open(r'C:\Users\matte\Downloads\workflow_api.json', 'r') as file:
    prompt = json.load(file)


if "114" in prompt:
    prompt["114"]["inputs"]["image"] = image_path
else:
    print("Sleutel '114' ontbreekt in de JSON-structuur.")


if "123" in prompt:
    prompt["123"]["inputs"]["text"] = text_prompt
else:
    print("Sleutel '123' ontbreekt in de JSON-structuur.")


ws = websocket.WebSocket()
ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
images = get_images(ws, prompt)
ws.close() # for in case this example is used in an environment where it will be repeatedly called, like in a Gradio app. otherwise, you'll randomly receive connection timeouts
#Commented out code to display the output images:

for node_id in images:
    for image_data in images[node_id]:
        from PIL import Image
        import io
        image = Image.open(io.BytesIO(image_data))
        image.show()

