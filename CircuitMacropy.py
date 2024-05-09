import eel
import eel.chrome
from json import load, dump
import os
from modules.createCircuitMacros import createCircuitMacros as csm
from tkinter import filedialog
from base64 import b64encode

projectPath = os.path.dirname(os.path.abspath(__file__))

def writeConf(data):
    with open(projectPath+'\\configurations.json', 'w', encoding='utf-8')as f:
        dump(data, f, indent=2, ensure_ascii=False)
def readConf():
    with open(projectPath+'\\configurations.json', encoding='utf-8')as f:
        return load(f)

@eel.expose
def createCircuitMacros():
    csm()
    return {'message': 'success'}

@eel.expose
def openfolder():
    conf = readConf()
    
    if not 'workspaceFolder' in list(conf.keys()):
        filepath = filedialog.askdirectory(title='Çalışacağınız Klasörü Seçiniz')
    else:
        if conf['workspaceFolder'] == '' or not os.path.exists(conf['workspaceFolder']):
            filepath = filedialog.askdirectory(title='Çalışacağınız Klasörü Seçiniz')
        else:
            filepath = conf['workspaceFolder']
    
    conf['workspaceFolder'] = filepath
    writeConf(conf)
    return filepath
@eel.expose
def getfiles(Path):
    allPath = []
    
    tree = os.walk(Path)
    
    for root, dirs, files in tree:
        if files != []:
            allPath.extend([{"path": Path.split('/')[-1], "dir": root.replace(Path, ''), 'file': a} for a in files])
        else:
            allPath.extend([{"path": Path.split('/')[-1], 'dir': root.replace(Path, ''), 'file': ''}])
    return allPath


@eel.expose
def getcontent(parent, file):
    for root, dirs, files in os.walk(readConf()['workspaceFolder']):
        if root.endswith(parent) and file in files:
            filename = os.path.join(root, file)
            with open(filename, encoding='utf-8')as f:
                return {'content': f.read(), 'fullpath': filename}
        if parent == "R0000T":
            with open(os.path.join(root, file), encoding='utf-8')as f:
                return {'content': f.read(), 'fullpath': os.path.join(root, file)}
    return '0'


@eel.expose
def getpdf(path):
    for root, dirs, files in os.walk(readConf()['workspaceFolder']):
        if root.endswith(path.split('\\')[1]) and path.split('\\')[2] in files:
            filename = os.path.join(root, path.split('\\')[2])
        elif path.split('\\')[1] == 'R0000T':
            filename = os.path.join(root, path.split('\\')[2])
    #return {'fullpath': filename}
    print(filename)
    with open(filename, 'rb')as f:
        return b64encode(f.read()).decode('utf-8')
    


"""
@app.route('/get_pdf', methods=['POST'])
def getPDF():
    if request.method == 'POST':
        path = request.json['path']
        print(path.split('\\'))
        print(path.split('/'))
        for root, dirs, files in walk(readConf()['workspaceFolder']):
            if root.endswith(path.split('\\')[1]) and path.split('\\')[2] in files:
                filename = os.path.join(root, path.split('\\')[2])
            elif path.split('\\')[1] == 'R0000T':
                filename = os.path.join(root, path.split('\\')[2])
        #return {'fullpath': filename}
        return send_file(filename)

"""


eel.init('assets')
eel.start('/html/main.html', size=(1366,743))