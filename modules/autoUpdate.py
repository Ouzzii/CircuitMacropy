from requests import get
import pygit2
version = 0.1

import os

print(os.getcwd())

def update():
    repo_url = 'https://github.com/Ouzzii/CircuitMacropy.git'
    local_dir = os.getcwd()
    repo = pygit2.clone_repository(repo_url, local_dir)
def checkUpdate(version):
    print("checking version")
    vars = {}
    updated_version = get('https://raw.githubusercontent.com/Ouzzii/CircuitMacropy/main/modules/autoUpdate.py').text
    exec(updated_version, vars)
    if vars[version] != version:
        update()
    else:
        print('CircuitMacropy is already up to date')
        





"""
import pygit2

# Klonlamak istediğiniz depo URL'si ve lokal dizin
repo_url = 'https://github.com/username/repository.git'
local_dir = '/path/to/save/repository'

# Depoyu klonlamak için
repo = pygit2.clone_repository(repo_url, local_dir)

print(f"Depo başarıyla klonlandı: {local_dir}")
"""