from requests import get
import shutil, os, pygit2
version = 0.1

def update():
    repo_url = 'https://github.com/Ouzzii/CircuitMacropy.git'
    local_dir = os.getcwd()
    shutil.rmtree(local_dir)
    os.mkdir(local_dir)
    repo = pygit2.clone_repository(repo_url, local_dir)

def checkUpdate(version):
    print("versiyon kontrolü yapılıyor")
    vars = {}
    updated_version = get('https://raw.githubusercontent.com/Ouzzii/CircuitMacropy/main/modules/autoUpdate.py').text
    exec(updated_version, vars)
    if vars[version] != version:
        print('CircuitMacropy güncelleniyor...')
        update()
    else:
        print('CircuitMacropy zaten güncel')
