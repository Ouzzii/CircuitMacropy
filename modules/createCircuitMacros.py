import os
from requests import get
from bs4 import BeautifulSoup as bs
from sys import platform
from json import dump, load
import zipfile


if platform != 'linux':
    if os.path.exists('/'.join(__file__.split('\\')[:-2])+'\\'):
        projectPath = '/'.join(__file__.split('\\')[:-2])+'\\'
    else:
        projectPath = '/'.join(__file__.split('\\')[:-2])+'\\..\\'
else:
    if os.path.exists('/'.join(__file__.split('/')[:-2])+'/'):
        projectPath = '/'.join(__file__.split('/')[:-2])+'/'
    else:
        '/'.join(__file__.split('/')[:-2])+'/../'



def writeConf(data):
    with open(projectPath+'configurations.json', 'w', encoding='utf-8')as f:
        dump(data, f, indent=2, ensure_ascii=False)
def readConf():
    with open(projectPath+'configurations.json', encoding='utf-8')as f:
        return load(f)

def createCircuitMacros():
    if platform != 'linux':
        if not os.path.exists(os.environ['USERPROFILE']+'\\CMEditor'):
            os.mkdir(os.environ['USERPROFILE']+'\\CMEditor')
        if len(os.listdir(os.environ['USERPROFILE']+'\\CMEditor')) == 0:
            circuitMacrosUrl = 'https://ece.uwaterloo.ca/~aplevich/Circuit_macros/'
            
            index = bs(get(circuitMacrosUrl).text, 'html.parser').find_all('a')
            for i in index:
                if i['href'].startswith('Circuit_macros') and i['href'].endswith('.zip'):
                    zip = i['href']
                    circuitmacrospath = os.environ['USERPROFILE']+'\\CMEditor\\'+zip.replace('.zip', '')
                    if not os.path.exists(circuitmacrospath):
                        os.mkdir(circuitmacrospath)
                    with open(circuitmacrospath+'\\'+zip, 'wb')as f:
                        f.write(get(circuitMacrosUrl+zip).content)
                    with zipfile.ZipFile(circuitmacrospath+'\\'+zip) as f:
                        f.extractall(circuitmacrospath)
                    os.remove(circuitmacrospath+'\\'+zip)
            dpicUrl = 'https://ece.uwaterloo.ca/~aplevich/dpic/Windows/dpic.exe'
            m4Url = 'https://ece.uwaterloo.ca/~aplevich/dpic/Windows/m4.exe'
            with open(circuitmacrospath+'\\m4.exe', 'wb')as f:
                f.write(get(m4Url).content)
            with open(circuitmacrospath+'\\dpic.exe', 'wb')as f:
                f.write(get(dpicUrl).content)
        else:
            circuitmacrospath = os.environ['USERPROFILE']+'\\CMEditor\\' + os.listdir(os.environ['USERPROFILE']+'\\CMEditor\\')[0]
    elif platform == 'linux':
        if not os.path.exists(os.environ['ZDOTDIR']+'/CMEditor'):
            os.mkdir(os.environ['ZDOTDIR']+'/CMEditor')
        if len(os.listdir(os.environ['ZDOTDIR']+'/CMEditor')) == 0:
            circuitMacrosUrl = 'https://ece.uwaterloo.ca/~aplevich/Circuit_macros/'
            
            index = bs(get(circuitMacrosUrl).text, 'html.parser').find_all('a')
            for i in index:
                if i['href'].startswith('Circuit_macros') and i['href'].endswith('.zip'):
                    zip = i['href']
                    circuitmacrospath = os.environ['ZDOTDIR']+'/CMEditor/'+zip.replace('.zip', '')
                    if not os.path.exists(circuitmacrospath):
                        os.mkdir(circuitmacrospath)
                    with open(circuitmacrospath+'\\'+zip, 'wb')as f:
                        f.write(get(circuitMacrosUrl+zip).content)
                    with zipfile.ZipFile(circuitmacrospath+'\\'+zip) as f:
                        f.extractall(circuitmacrospath)
                    os.remove(circuitmacrospath+'\\'+zip)
            #dpicUrl = 'https://ece.uwaterloo.ca/~aplevich/dpic/Windows/dpic.exe'
            #m4Url = 'https://ece.uwaterloo.ca/~aplevich/dpic/Windows/m4.exe'
            #with open(circuitmacrospath+'/m4.exe', 'wb')as f:
            #    f.write(get(m4Url).content)
            #with open(circuitmacrospath+'/dpic.exe', 'wb')as f:
            #    f.write(get(dpicUrl).content)
        else:
            circuitmacrospath = os.environ['ZDOTDIR']+'/CMEditor/' + os.listdir(os.environ['ZDOTDIR']+'/CMEditor/')[-1]
    conf = readConf()
    if platform == 'linux':
        conf['dpicengine'] = 'dpic'
        conf['m4engine'] = 'm4'
    else:
        conf['dpicengine'] = 'dpic.exe'
        conf['m4engine'] = 'm4.exe'
    conf['m4flag'] = 'pgf.m4'
    
    conf['dpicflag'] = '-g'
    conf['CircuitMacrosPath'] = circuitmacrospath
    
    writeConf(conf)
    return {'message': 'succesful'}
