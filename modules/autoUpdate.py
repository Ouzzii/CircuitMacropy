from requests import get
import shutil, os, pygit2
import zipfile
import io
version = 0.1


def clearDirectory(local_dir):
    for content in os.listdir(local_dir):
        if os.path.isfile(os.path.join(local_dir, content)):
            os.remove(os.path.join(local_dir, content))
        else:
            shutil.rmtree(os.path.join(local_dir, content))

def download_and_extract_specific_folder(repo_url, extract_to):
    # Geçici dizin oluştur
    temp_dir = os.path.join(extract_to, 'temp_repo')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # GitHub API'si aracılığıyla zip dosyasının URL'sini oluşturun
    if repo_url.endswith('.git'):
        repo_url = repo_url[:-4]
    zip_url = f"{repo_url}/archive/refs/heads/main.zip"
    
    # Zip dosyasını indirin
    print(f"{zip_url} indiriliyor...")
    response = get(zip_url)
    response.raise_for_status()
    
    # Zip dosyasını belleğe yükleyin ve geçici dizine çıkartın
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
        zip_file.extractall(temp_dir)
        print(f"İçerik geçici dizine çıkarıldı: {temp_dir}")
    
    # İndirilen klasördeki belirli bir klasörün dosyalarını al
    extracted_folder_name = os.path.basename(repo_url) + '-main'
    specific_folder_path = os.path.join(temp_dir, extracted_folder_name)
    
    # Belirli klasördeki dosyaları hedef dizine taşı
    for item in os.listdir(specific_folder_path):
        s = os.path.join(specific_folder_path, item)
        d = os.path.join(extract_to, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
    
    # Geçici dizini sil
    shutil.rmtree(temp_dir)
    print(f"Dosyalar {specific_folder_path} dizininden {extract_to} dizinine taşındı.")

def update():
    repo_url = 'https://github.com/Ouzzii/CircuitMacropy.git'
    local_dir = os.getcwd()
    clearDirectory(local_dir)
    download_and_extract_specific_folder(repo_url, local_dir)
    #pygit2.clone_repository(repo_url, local_dir)


def checkUpdate(version):
    print("versiyon kontrolü yapılıyor")
    vars = {}
    updated_version = get('https://raw.githubusercontent.com/Ouzzii/CircuitMacropy/main/modules/autoUpdate.py').text
    exec(updated_version, vars)
    if vars['version'] > version:
        print('CircuitMacropy güncelleniyor...')
        update()
    else:
        print('CircuitMacropy zaten güncel')
