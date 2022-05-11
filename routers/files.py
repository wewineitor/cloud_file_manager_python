from fastapi import APIRouter, status, HTTPException, UploadFile, File, Form
import os
import math
from dotenv import load_dotenv
load_dotenv()

router:APIRouter = APIRouter()

CLOUD_PATH:str = os.getenv('CLOUD_PATH')

def get_path(path:str) -> str:
    """
    Se encarga de definir la ruta adecuada donde se va a trabajar

    Args:
        path (str): Es la ruta inicial para definir si trabajara en la raiz o dentro de una carpeta
    
    Returns:
        str:  Retorna la ruta completa donde se va a trabajar
    """
    if path == '':
        path = CLOUD_PATH
    else :
        path_formated = path.replace('-', '/')
        path = f'{CLOUD_PATH}{path_formated}'
    return path

@router.post('/uploadFile/', status_code = status.HTTP_200_OK)
def upload_file(path_param:str = '', upload_file:UploadFile = File(...)) -> dict:
    """
    Se encarga de cargar los archivos en la ruta que se encuentre

    Args:
        path_param (str): Es la ruta inicial para definir si trabajara en la raiz o dentro de una carpeta
        upload_file (UploadFile): Es el archivo cargado mediante un formulario 
        el cual se almacenara en la ruta especificada
    
    Returns:
        dict:  Retorna la respuesta del status que se mostrara en un formato json
    """
    path:str = get_path(path_param)
    with open(f'{path}/{upload_file.filename}', 'wb') as file_object:
        file_object.write(upload_file.file.read())
        file_object.close()
    return {"status": "ok"}

@router.get('/getFiles/', status_code = status.HTTP_200_OK)
def get_files(path_param:str = '') -> dict:
    """
    Se encarga de obtener los archivos y carpetas que se encuentran en la ruta especificada

    Args:
        path_param (str): Es la ruta inicial para definir si trabajara en la raiz o dentro de una carpeta
    
    Returns:
        dict: Retorna los archivos de la ruta junto con su tamaño en KB en un formato json
    """
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
def create_folder(path_param:str = '', new_folder = Form(...)) -> dict:
    """
    Se encarga de crear el folder en la ruta especificada

    Args:
        path_param (str): Es la ruta inicial para definir si trabajara en la raiz o dentro de una carpeta
        new_forlder (Form): Es el nuevo folder que se creara dentro de la ruta especificada
    
    Returns:
        dict:  Retorna la respuesta del status que se mostrara en un formato json
    """
    path:str = get_path(path_param)
    try:
        os.mkdir(f'{path}/{new_folder}')
    except FileExistsError:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail = "don't create folders with the same name")
    return {"status": "ok"}
