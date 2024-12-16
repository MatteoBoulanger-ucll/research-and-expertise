import websocket
import uuid
import json
import urllib.request
import urllib.parse
from PIL import Image
import io
import os
import shutil
import sys

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())

# Read arguments: sys.argv[1] = text_prompt, sys.argv[2] = image_path
if len(sys.argv) < 3:
    print("Usage: python websockets_api.py <text_prompt> <image_path>")
    sys.exit(1)

text_prompt = sys.argv[1]
image_path = sys.argv[2]

if not os.path.isfile(image_path):
    print("Invalid image file.")
    sys.exit(1)

def clear_output_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)

output_folder = "C:/Users/Jornick/Documents/comf/ComfyUI_windows_portable/ComfyUI/output"
clear_output_folder(output_folder)

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
                    break
        else:
            continue

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

script_dir = os.path.dirname(os.path.abspath(__file__))
workflow_api_path = os.path.join(script_dir, 'workflow_api.json')

with open(workflow_api_path, 'r') as file:
    prompt = json.load(file)

# Set the image_path and text_prompt in the JSON
if "254" in prompt:
    prompt["254"]["inputs"]["image"] = image_path
else:
    print("Key '254' not found in JSON structure.")

if "123" in prompt:
    prompt["123"]["inputs"]["text"] = text_prompt
else:
    print("Key '123' not found in JSON structure.")

ws = websocket.WebSocket()
ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
images = get_images(ws, prompt)
ws.close()
