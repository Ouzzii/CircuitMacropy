from requests import get

version = 0.2

def checkUpdate(version):
    vars = {}
    updated_version = get('https://raw.githubusercontent.com/Ouzzii/CircuitMacropy/main/modules/autoUpdate.py').text
    exec(updated_version, vars)
    print(vars['version'])
checkUpdate(version)