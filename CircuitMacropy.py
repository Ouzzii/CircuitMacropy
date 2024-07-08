# pip install Eel requests bs4
for i in range(2):
    try:
        import eel
        import eel.chrome
        from json import load, dump
        import os
        from modules.createCircuitMacros import createCircuitMacros as csm
        from tkinter import filedialog
        from base64 import b64encode
        from subprocess import Popen, PIPE
        from sys import platform
        break
    except ImportError:
        import os
        os.system('python3.10 -m pip install Eel requests bs4')

if ".pyz" in __file__:
    projectPath = os.path.dirname(os.path.abspath("CircuitMacropy.pyz"))
else:
    projectPath = os.path.dirname(os.path.abspath(__file__))

global pdflatex_path





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
def getJunkFiles():
    conf = readConf()
    if 'junkfiles' in list(conf.keys()):
        return conf['junkfiles']
    else:
        return ''

@eel.expose
def applySettings(junkfiles):
    
    conf = readConf()
    conf['junkfiles'] = junkfiles
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