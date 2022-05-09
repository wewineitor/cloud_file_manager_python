from importlib.metadata import files
from fastapi import APIRouter, status, HTTPException, UploadFile, File, Form
import os
import math

router:APIRouter = APIRouter()

CLOUD_PATH:str = 'C:/Users/Edwin/Desktop/nube/'

def get_path(path:str) -> str:
    """
    Se encarga de definir la ruta adecuada donde se va a trabajar

    Args:
        path (str): Es la ruta inicial para
    
    Returns:
        str:  Return the path where the files will be saved or new directory will be create
    """
    if path == '':
        path = CLOUD_PATH
    else :
        path_formated = path.replace('-', '/')
        path = f'{CLOUD_PATH}/{path_formated}'
    return path

@router.post('/uploadFile/', status_code = status.HTTP_200_OK)
def upload_file(path_param:str = '', upload_file:UploadFile = File(...)) -> dict:
    """
    Permite cargar archivos en la ruta seleccionada
    """
    path:str = get_path(path_param)
    with open(f'{path}/{upload_file.filename}', 'wb') as file_object:
        file_object.write(upload_file.file.read())
        file_object.close()
    return {"status": "ok"}

@router.get('/getFiles/', status_code = status.HTTP_200_OK)
def get_files(path_param:str = ''):
    path:str = get_path(path_param)
    files_list:list = os.listdir(path)
    files:list = []
    for f in files_list:
        files.append({
            "name": f,
            "size": math.ceil(os.path.getsize(f'{path}{f}') / 1024)
        })
    
    return {"files": files}

@router.post('/createFolder/', status_code=status.HTTP_201_CREATED)
def create_folder(path_param:str = '', new_folder = Form(...)):
    path:str = get_path(path_param)
    try:
        os.mkdir(f'{path}/{new_folder}')
    except FileExistsError:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail = "don't create folders with the same name")
    return {"status": "ok"}
