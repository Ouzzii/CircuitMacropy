from requests import get
import shutil, os
import zipfile
import io
from .checkConnection import internet_connection
version = 0.2


def clearDirectory(local_dir):
    for content in os.listdir(local_dir):
        if os.path.isfile(os.path.join(local_dir, content)):
            os.remove(os.path.join(local_dir, content))
        else:
            shutil.rmtree(os.path.join(local_dir, content))

def download_and_extract_specific_folder(repo_url, extract_to):

    temp_dir = os.path.join(extract_to, 'temp_repo')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    if repo_url.endswith('.git'):
        repo_url = repo_url[:-4]
    zip_url = f"{repo_url}/archive/refs/heads/main.zip"
    
    response = get(zip_url)
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
        zip_file.extractall(temp_dir)
    
    extracted_folder_name = os.path.basename(repo_url) + '-main'
    specific_folder_path = os.path.join(temp_dir, extracted_folder_name)
    
    for item in os.listdir(specific_folder_path):
        s = os.path.join(specific_folder_path, item)
        d = os.path.join(extract_to, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
    
    shutil.rmtree(temp_dir)

def update():
    print('CircuitMacropy güncelleniyor')
    repo_url = 'https://github.com/Ouzzii/CircuitMacropy.git'
    local_dir = os.getcwd()
    clearDirectory(local_dir)
    download_and_extract_specific_folder(repo_url, local_dir)


def checkUpdate(version):
    if internet_connection():
        print("versiyon kontrolü yapılıyor")
        vars = {}
        updated_version = get('https://raw.githubusercontent.com/Ouzzii/CircuitMacropy/main/modules/autoUpdate.py').text
        exec(updated_version, vars)
        if vars['version'] > version:
            print('CircuitMacropy güncellenmeye hazır')
            return 'update_available'
        else:
            print('CircuitMacropy zaten güncel')
            return 'up_to_date'
    else:
        return "no_connection"
