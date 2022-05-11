import os
from fastapi.testclient import TestClient
import files
from dotenv import load_dotenv
import math
load_dotenv()

CLOUD_PATH:str = os.getenv('CLOUD_PATH')

test = TestClient(files.router)

def test_get_path():
    assert files.get_path('') == CLOUD_PATH
    assert files.get_path('asd-') == f'{CLOUD_PATH}asd/'
    assert files.get_path('asd-carpeta-') == f'{CLOUD_PATH}asd/carpeta/'

def test_upload_files():
    file_name:str = "app.py"
    file = open(f"./{file_name}", "rb")
    file_upload = (file_name, file)
    response = test.post('/uploadFile/', files={"upload_file": file_upload})
    file.close()
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    os.remove(f"C:/Users/Edwin/Desktop/nube/{file_name}")

def test_get_files():
    response = test.get('/getFiles')

    path:str = files.get_path('')
    files_list:list = os.listdir(path)
    files_json:list = []
    for f in files_list:
        files_json.append({
            "name": f,
            "size": math.ceil(os.path.getsize(f'{path}{f}') / 1024)
        })

    assert response.status_code == 200
    assert response.json() == {'files': files_json}

def test_create_folder():
    response = test.post('/createFolder/', data=[("new_folder", "carpeta")])
    assert response.status_code == 201
    assert response.json() == {"status": "ok"}


