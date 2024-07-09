# pip install Eel requests bs4
for i in range(2):
    try:
        import eel
        import eel.chrome
        from json import load, dump
        import os
        from tkinter import filedialog
        from base64 import b64encode
        from subprocess import Popen, PIPE
        from sys import platform
        break
    except ImportError:
        import os
        os.system('py -3.10 -m pip install Eel requests bs4')

from modules.createCircuitMacros import createCircuitMacros as csm
from modules.autoUpdate import checkUpdate, version, update

if ".pyz" in __file__:
    projectPath = os.path.dirname(os.path.abspath("CircuitMacropy.pyz"))
else:
    projectPath = os.path.dirname(os.path.abspath(__file__))

global pdflatex_path
global ask_for_update


if platform == 'linux':
    m4executable = 'm4'
    dpicexecutable = 'dpic'
elif platform == 'win32':
    m4executable = 'm4.exe'
    dpicexecutable = 'dpic.exe'
    stdout, stderr = Popen(f'where pdflatex', shell=True, stdout=PIPE, stderr=PIPE).communicate()
    pdflatex_path = stdout.decode('utf-8').split('\n')[0]



with open('info.json', encoding='utf-8')as f:
    infoJson = load(f)

def writeConf(data):
    if platform != 'linux':
        with open(projectPath+'\\configurations.json', 'w', encoding='utf-8')as f:
            dump(data, f, indent=2, ensure_ascii=False)
    else:
        with open(projectPath+'/configurations.json', 'w', encoding='utf-8')as f:
            dump(data, f, indent=2, ensure_ascii=False)
def readConf():
    if platform != 'linux':
        with open(projectPath+'\\configurations.json', encoding='utf-8')as f:
            return load(f)
    else:
        with open(projectPath+'/configurations.json', encoding='utf-8')as f:
            return load(f)


conf = readConf()
checked = checkUpdate(version)
if 'autoupdate' in list(conf.keys()):
    ask_for_update = False
    otoupdate = conf['autoupdate']
    if otoupdate and checked == 'update_available':
        update()
    elif not otoupdate and checked == 'update_available':
        ask_for_update = True

else:
    ask_for_update = False
    otoupdate = True
    conf['autoupdate'] = True
    writeConf(conf)
    if checked == 'update_available':
        update()
    
def clearJunkFiles():
    conf = readConf()
    junkext = conf['junkfiles'].split(',')
    for root, folder, files in os.walk(conf['workspaceFolder']):
        for file in files:
            if '.'+file.split('.')[-1] in junkext:
                os.remove(root + '/' + file)

@eel.expose
def createCircuitMacros():
    csm()
    return {'message': 'success'}

@eel.expose
def getinfo(infoname):
    return infoJson[infoname]

@eel.expose
def filesettings():
    conf = readConf()
    if 'junkfiles' in list(conf.keys()):
        return conf['junkfiles']
    else:
        return ''
@eel.expose
def updatesettings(): 
    conf = readConf()
    if 'autoupdate' in list(conf.keys()):
        return conf['autoupdate']
    else:
        conf['autoupdate'] = False
        writeConf(conf)
        return False
    
    
@eel.expose
def applySettings(junkfiles, autoupdate):
    # Junkfiles
    conf = readConf()
    conf['junkfiles'] = junkfiles
    
    #autoupdate
    conf['autoupdate'] = autoupdate
    
    writeConf(conf)
    
    
@eel.expose
def getSettings():
    with open('assets/html/settings.html', encoding='utf-8') as f:
        return f.read()
    
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



@eel.expose
def saveContent(path, content):
    with open(path, 'w', encoding='utf-8')as f:
        f.write(content)

@eel.expose
def compile(basecontent, compileas, compileto):
    conf = readConf()
    print(os.getcwd())
    if compileto == 'latex':
        if compileas == 'pgf':
            os.chdir(conf['CircuitMacrosPath'])
            print(os.getcwd())
            texfile = basecontent.split('.')[0]+".tex"
            compiledContent = Popen(f"{m4executable} {compileas}.m4 {basecontent} | {dpicexecutable} -g", stdout=PIPE, shell=True).stdout.read()
            with open(texfile, 'wb')as f:
                f.write(compiledContent)
    elif compileto == 'pdf':
        if basecontent.endswith('.tex'):
            os.chdir(conf['workspaceFolder'])
            print(f'{pdflatex_path} -interaction=nonstopmode {basecontent}')
            Popen(f'{pdflatex_path} -interaction=nonstopmode {basecontent}', shell=True).communicate()
        else:
            os.chdir(conf['CircuitMacrosPath'])
            texfile = basecontent.split('.')[0]+".tex"
            compiledContent = Popen(f"{m4executable} {compileas}.m4 {basecontent} | {dpicexecutable} -g", stdout=PIPE, shell=True).stdout.read()
            print(f"{m4executable} {compileas}.m4 {basecontent} | {dpicexecutable} -g")
            with open(texfile, 'wb')as f:
                f.write(compiledContent)
            os.chdir(readConf()['workspaceFolder'])
            Popen(fr'{pdflatex_path} -interaction=nonstopmode {texfile.replace(chr(92), "/")}', shell=True).communicate()
    clearJunkFiles()
    os.chdir(projectPath)
    return {'message': 'compiled'}

@eel.expose
def getWorkspaceFolder():
    conf = readConf()
    return conf['workspaceFolder']


@eel.expose
def saveFile(filename):
    conf = readConf()
    print('save file çalıştı')
    print(os.path.join(conf['workspaceFolder'], filename))
    with open(os.path.join(conf['workspaceFolder'], filename), 'w')as f:
        f.write('')
    return {'message': 'file created'}

@eel.expose
def clearWorkspace():
    conf = readConf()
    conf['workspaceFolder'] = ""
    writeConf(conf)
    
@eel.expose
def getColorPalette(key):
    if platform != 'linux':
        with open(projectPath+'\\colorPalette.json', encoding='utf-8')as f:
            return load(f)[key]
    else:
        with open(projectPath+'/colorPalette.json', encoding='utf-8')as f:
            return load(f)[key]

@eel.expose
def Is_there_an_update_available():
    if ask_for_update:
        with open('assets/html/ask_for_update.html', encoding='utf-8')as f:
            return f.read()
    else:
        return False

@eel.expose
def update_():
    update()

def detect_pdflatex_version():
    if platform == 'win32':
        global pdflatex_path
        stdout, stderr = Popen(fr'where pdflatex', shell=True, stdout=PIPE, stderr=PIPE).communicate()
        pdflatex_path = stdout.decode('utf-8').split('\n')[0]


    compilers = ['MiKTeX', 'texlive', 'PCTeX', 'BaKoMa TeX']

    conf = readConf()
    for i in compilers:
        if i in pdflatex_path:
            conf['pdflatex_version'] = i
            writeConf(conf)
    return conf['pdflatex_version']





eel.init('assets')
#eel.start('/html/main.html', size=(1366,743))
eel.start('/html/main.html', size=(960,520))
#eel.start('/html/main.html', size=(1920,1080))