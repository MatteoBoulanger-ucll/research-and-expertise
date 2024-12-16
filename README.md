# research-and-expertise

backend:  python -m uvicorn server:app --reload

frontend: npm run start

Changes need to be made in 

websockets_api.py
on line 41

output_folder = "YOUR COMFYUI OUTPUT FOLDER"


inorder to start project 

python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
