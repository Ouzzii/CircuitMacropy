import os
from requests import get
from bs4 import BeautifulSoup as bs
from sys import platform
from pathlib import Path
from json import dump, load
import zipfile

from modules.configuration_utils import readConf, writeConf

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


def createCircuitMacros():
    if platform == 'win32':
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
        if not os.path.exists(os.environ['HOME']+'/CMEditor'):
            os.mkdir(os.environ['HOME']+'/CMEditor')
        if len(os.listdir(os.environ['HOME']+'/CMEditor')) == 0:
            circuitMacrosUrl = 'https://ece.uwaterloo.ca/~aplevich/Circuit_macros/'
            
            index = bs(get(circuitMacrosUrl).text, 'html.parser').find_all('a')
            for i in index:
                if i['href'].startswith('Circuit_macros') and i['href'].endswith('.zip'):
                    zip = i['href']
                    circuitmacrospath = os.environ['HOME']+'/CMEditor/'+zip.replace('.zip', '')
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
            circuitmacrospath = os.environ['HOME']+'/CMEditor/' + os.listdir(os.environ['HOME']+'/CMEditor/')[-1]
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
