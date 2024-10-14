# pip install Eel requests bs4
import os
# List of required packages
required_packages = ['eel', 'requests', 'bs4']

# Function to install missing packages
def install_packages(packages):
    os.system('py -3.10 -m pip install ' + ' '.join(packages))

# Check for missing packages
missing_packages = []
for package in required_packages:
    try:
        __import__(package)
    except ModuleNotFoundError:
        missing_packages.append(package)

# Install missing packages if any
if missing_packages:
    install_packages(missing_packages)

# Import modules after ensuring all are installed
import eel
import eel.chrome
from json import load, dump
from tkinter import filedialog
from base64 import b64encode
from subprocess import Popen, PIPE
import subprocess, git
from sys import platform

from modules.createCircuitMacros import createCircuitMacros as csm
from modules.autoUpdate import checkUpdate, version, update
from modules.detect_tex_distros import detect_tex_distros, detect_boxdims_is_installed
from modules.configuration_utils import readConf, writeConf
from modules.checkConnection import internet_connection
#from modules import detect_tex_distros

from datetime import datetime
import socket, logging
from modules.configuration_utils import setup_logging
setup_logging()
logger = logging.getLogger(__name__)

if ".pyz" in __file__:
    projectPath = os.path.dirname(os.path.abspath("CircuitMacropy.pyz"))
else:
    projectPath = os.path.dirname(os.path.abspath(__file__))





global ask_for_update
global checked


ask_for_update = True

if platform == 'linux':
    m4executable = 'm4'
    dpicexecutable = 'dpic'
elif platform == 'win32':
    m4executable = 'm4.exe'
    dpicexecutable = 'dpic.exe'


if platform == 'win32':
    with open(projectPath + '\\info.json', encoding='utf-8')as f:
        infoJson = load(f)
elif platform == 'linux':
    with open(projectPath + '/info.json', encoding='utf-8')as f:
        infoJson = load(f)



#check git repo
if not os.path.exists('./.git'):
    if internet_connection():
        logger.debug('Git klasörü oluşturuldu.')
        repo = git.Repo.init('./')
        repo.create_remote('origin', 'https://github.com/Ouzzii/CircuitMacropy.git')
    else:
        logger.error('İnternet olmadığından git klasörü oluşturulamadı')
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
def getLaTeXSettings():
    conf = readConf()
    availableTexDistros = list(conf['pdflatex-paths'].keys())
    if 'last-distro' in list(conf.keys()):
        selectedPdflatexPath = conf["last-distro"]
    else:
        selectedPdflatexPath = None
    seletcedTexDistro = next((key for key, value in conf["pdflatex-paths"].items() if value == conf["last-distro"]), None)
    availablePdflatexPaths = list(conf['pdflatex-paths'].values())
    
    return {
        'message': 'success',
        'availableTexDistros': availableTexDistros,
        'selectedPdflatexPath': selectedPdflatexPath,
        'selectedTexDistro': seletcedTexDistro,
        'availablePdflatexPaths': availablePdflatexPaths
    }
    
    
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
def applySettings(junkfiles, autoupdate, selectedPdflatexPath):
    # Junkfiles
    conf = readConf()
    conf['junkfiles'] = junkfiles
    
    #autoupdate
    conf['autoupdate'] = autoupdate
    
    conf['last-distro'] = selectedPdflatexPath
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
        filename = ''
        if root.endswith(parent) and file in files:
            filename = os.path.join(root, file)
        if parent == "R0000T":
            filename = os.path.join(root, file)
        if os.path.exists(filename):
            with open(filename, encoding='utf-8')as f:
                return {'content': f.read(), 'fullpath': filename}
    return '0'


@eel.expose
def getpdf(path):
    for root, dirs, files in os.walk(readConf()['workspaceFolder']):       
        if root.endswith(path.split('\\')[1]) and path.split('\\')[2] in files:
            filename = os.path.join(root, path.split('\\')[2])
        elif path.split('\\')[1] == 'R0000T':
            filename = os.path.join(root, '\\'.join(path.split('\\')[2:]))
        if os.path.exists(filename):
            break
    #return {'fullpath': filename}
    with open(filename, 'rb')as f:
        return b64encode(f.read()).decode('utf-8')



@eel.expose
def saveContent(path, content):
    with open(path, 'w', encoding='utf-8')as f:
        f.write(content)
    return {'message': 'success'}

@eel.expose
def compile(basecontent, compileas, compileto):
    conf = readConf()
    logger.debug(f'{basecontent}: compiling from {compileas} to {compileto}')
    basecontent = os.path.join(basecontent)
    if compileto == 'latex':
        if compileas == 'pgf':
            os.chdir(conf['CircuitMacrosPath'])
            texfile = basecontent.split('.')[0]+".tex"
            m4_stdout, m4_stderr = Popen(f"{m4executable} {compileas}.m4 {basecontent} | {dpicexecutable} -g", shell=True, stdout=PIPE, stderr = PIPE).communicate()
            m4_stdout = m4_stdout.decode('utf-8')
            with open(texfile, 'w')as f:
                f.write(m4_stdout)
    elif compileto == 'pdf':
        if basecontent.endswith('.tex'):
            os.chdir(conf['workspaceFolder'])
            pdflatex_stdout, pdflatex_stderr = Popen(f'{conf["last-distro"]} -interaction=nonstopmode {basecontent}', shell=True).communicate()
            pdflatex_stdout = pdflatex_stdout.decode('utf-8')
        else:
            os.chdir(conf['CircuitMacrosPath'])
            texfile = os.path.splitext(basecontent)[0]+".tex"
            m4_stdout, m4_stderr = Popen(f"{m4executable} {compileas}.m4 {basecontent} | {dpicexecutable} -g", shell=True, stdout = PIPE, stderr = PIPE).communicate()
            m4_stdout  = m4_stdout.decode('utf-8')
            with open(texfile, 'w')as f:
                f.write(m4_stdout)
            os.chdir(readConf()['workspaceFolder'])
            pdflatex_stdout, pdflatex_stderr = Popen(rf'{conf["last-distro"]} -interaction=nonstopmode {texfile.replace(chr(92), "/")}', shell=True, stdout = PIPE, stderr = PIPE).communicate()
            pdflatex_stdout = pdflatex_stdout.decode('utf-8')
    clearJunkFiles()
    os.chdir(projectPath)
    
    print(m4_stdout)
    print(pdflatex_stdout)
    
    if compileto == 'pdf' and 'Output written on' in pdflatex_stdout:
        return {'message': 'compile successful',
                'notification': 'Dosya basariyla derlendi'}
    if compileto == 'pdf' and not 'Output written on' in pdflatex_stdout:
        return {'message': 'compile not successful',
                'notification': 'Dosya derlenirken bir hata meydana geldi, hata ayrintisi icin hata kayitlarina bakabilirsiniz'}

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

@eel.expose
def Is_there_an_update_available():
    if ask_for_update:
        with open('assets/html/ask_for_update.html', encoding='utf-8')as f:
            return {'message': 'update available',
                    'html_content': f.read()}
    elif ask_for_update == False and checked == "no_connection":
        with open('assets/html/no_connection.html', encoding='utf-8')as f:
            return {'message': 'no internet connection',
                    'html_content': f.read()}
    else:
        return {'message': 'already up to date',
                'html_content': ''}


@eel.expose
def update_():
    update()

def detect_pdflatex_version():
    global pdflatex_path
    if platform == 'win32':
        stdout, stderr = Popen(fr'where pdflatex', shell=True, stdout=PIPE, stderr=PIPE).communicate()
        pdflatex_path = stdout.decode('utf-8').split('\n')[0]
    elif platform == 'linux':
        stdout, stderr = Popen(fr'which pdflatex', shell=True, stdout=PIPE, stderr=PIPE).communicate()
        pdflatex_path = stdout.decode('utf-8').split('\n')[0]
        
        
    if platform == 'win32':
        compilers = ['MiKTeX', 'texlive', 'PCTeX', 'BaKoMa TeX']

        conf = readConf()
        for i in compilers:
            if i in pdflatex_path:
                conf['pdflatex_version'] = i
                writeConf(conf)
        return conf['pdflatex_version']
    elif platform == 'linux':
        compilers = ['MiKTeX', 'texlive', 'PCTeX', 'BaKoMa TeX']

        conf = readConf()
        for i in compilers:
            if i in pdflatex_path:
                conf['pdflatex_version'] = i
                writeConf(conf)
        return conf['pdflatex_version']



def initialization():
    pass

@eel.expose
def getSessionLogs():
    logs = os.listdir('./logs/')
    return logs
    #with open(f'./logs/{datetime.now().strftime("%Y-%m-%d")}.log', encoding="utf-8")as f:
    #    for i in  f.readlines():
    #        log.append(
    #            [
    #                i.split(" - ")[0],
    #                i.split(" - ")[1],
    #                i.split(" - ")[2],
    #                i.split(" - ")[3]
    #            ]
    #        )
    #return log
@eel.expose
def getSessionLog(logname):
    log = []
    with open(f'./logs/{logname}', encoding="utf-8")as f:
        for i in  f.readlines():
            try:
                log.append(
                    [
                        i.split(" - ")[0],
                        i.split(" - ")[1],
                        i.split(" - ")[2],
                        i.split(" - ")[3]
                    ]
                )
            except IndexError:
                log.append([i])
    return log
    
@eel.expose
def select_distro(distro):
    conf = readConf()
    conf['last-distro'] = conf['pdflatex-paths'][distro]
    writeConf(conf)
@eel.expose
def check_selected_distro():
    conf = readConf()
    if not 'last-distro' in list(conf.keys()):
        return False
    elif conf['last-distro']:
        return True

if __name__ == '__main__':    
    conf = readConf()
    checked = checkUpdate(version)
    if checked != "no_connection":
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
    else:
        ask_for_update = False

    #detect_pdflatex_version()
    #detect_tex_distros()
    
    
    eel.init('assets')
    #eel.start('/html/main.html', size=(1366,743))
    eel.start('/html/main.html', size=(960,520))
    #eel.start('/html/main.html', size=(1920,1080))
