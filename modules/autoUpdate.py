from requests import get
import shutil, os, pygit2
version = 0.1

print('a')
def clearDirectory(local_dir):
    for content in os.listdir(local_dir):
        if os.path.isfile(os.path.join(local_dir, content)):
            os.remove(os.path.join(local_dir, content))
        else:
            shutil.rmtree(os.path.join(local_dir, content))

def move_all_files_and_folders(src_dir, dest_dir):
    # Kaynak dizindeki tüm dosya ve klasörlerin listesini al
    items = os.listdir(src_dir)
    
    for item in items:
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)
        
        # Dosya veya klasörü hedef dizine taşı
        shutil.move(src_path, dest_path)
        print(f"Taşındı: {src_path} -> {dest_path}")

def update():
    repo_url = 'https://github.com/Ouzzii/CircuitMacropy.git'
    local_dir = os.getcwd()
    shutil.rmtree(local_dir)
    os.mkdir(local_dir)
    pygit2.clone_repository(repo_url, local_dir)


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
