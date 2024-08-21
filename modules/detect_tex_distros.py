from subprocess import Popen, PIPE
from pathlib import Path
import sys, os, requests, zipfile
import eel, logging

from modules.checkConnection import internet_connection
from modules.configuration_utils import readConf, writeConf, setup_logging

setup_logging()
logger = logging.getLogger(__name__)


@eel.expose
def detect_tex_distros():
    conf = readConf()
    if not 'pdflatex-paths' in list(conf.keys()):
        conf['pdflatex-paths'] = {}
    
    
    
    if 'last-distro' in list(conf.keys()):
        if conf['last-distro'] != '':
            key = next((key for key, value in conf["pdflatex-paths"].items() if value == conf["last-distro"]), None)
            return [key, '']
    
    
    #checking for miktex
    logger.debug('Miktex kontrol ediliyor')
    if sys.platform == 'linux':
        #stdout, stderr = Popen('find / -name miktex-pdftex 2>&1 | grep -v "Permission denied" | grep -v "Invalid argument" | grep -v "No such file or directory"', shell=True, stdout=PIPE, stderr=PIPE).communicate()
        stdout, stderr = Popen('find / -name miktex-pdflatex 2>&1 | grep -v "Permission denied" | grep -v "Invalid argument" | grep -v "No such file or directory"', shell=True, stdout=PIPE, stderr=PIPE).communicate()
        
        path = stdout.decode('utf-8').strip()
        if path:
            conf['pdflatex-paths']['miktex'] = path
            #detect_boxdims_is_installed()
        logger.debug('Diğer TeX dağıtımları kontrol ediliyor')
        stdout, stderr = Popen('which pdflatex', shell = True, stdout = PIPE, stderr= PIPE).communicate()
        path = stdout.decode('utf-8').strip().split('\n')[0]
        if path:
            stdout, stderr = Popen(f'{path} --version', shell = True, stdout = PIPE, stderr = PIPE).communicate()
            if 'TeX Live' in stdout.decode('utf-8').strip():
                conf['pdflatex-paths']['texlive'] = path
            
        return [writeConf(conf), detect_boxdims_is_installed()]
    elif sys.platform == 'win32':
        logger.debug('Tex Dagitimlari Kontrol Ediliyor')
        stdout, stderr = Popen('where pdflatex', shell = True, stdout = PIPE, stderr = PIPE).communicate()
        path = stdout.decode('utf-8').split('\n')
        for distro in path:
            stdout, stderr = Popen(f'{distro} --version', shell = True, stdout = PIPE, stderr = True).communicate()
            log = stdout.decode('utf-8').strip()
            
            if 'MiKTeX-pdfTeX' in log:
                conf['pdflatex-paths']['miktex'] = distro.strip()
            elif 'TeX Live' in log:
                conf['pdflatex-paths']['texlive'] = distro.strip()
        return [writeConf(conf), detect_boxdims_is_installed()]

def detect_boxdims_is_installed():
    conf = readConf()
    result = {}
    if sys.platform == 'linux':
        logger.debug('Miktex için boxdims.sty kontrolü yapılıyor')
        if 'miktex' in list(conf['pdflatex-paths'].keys()):
            miktex_path = os.path.join(os.environ['HOME'], '.miktex', 'texmfs', 'install', 'tex', 'latex', 'circuit_macros')
            if not os.path.exists(miktex_path):
                if internet_connection():
                    with open(miktex_path + '.zip', 'wb')as f:
                        f.write(requests.get('https://mirrors.ctan.org/graphics/circuit_macros.zip').content)
                    
                    #print(Path(miktex_path).parent)
                    with zipfile.ZipFile(miktex_path + '.zip', 'r') as zip_ref:
                        zip_ref.extractall(Path(miktex_path).parent)
                        os.remove(miktex_path + '.zip')
                    Popen(f'{get_initexmf()} --update-fndb', shell=True, stdout = PIPE, stderr = PIPE).communicate()
                    logger.info('Miktex: boxdims.sty başarılı bir şekilde indirildi')
                    result['miktex'] = True
                else:
                    result['miktex'] = False
                    logger.error('Miktex: internet bağlantısı olmadığından boxdims.sty indirilemedi')
            else:
                result['miktex'] = True
                logger.info('Miktex: boxdims.sty zaten kurulu')
        
        # PERMİSSİON ERROR OR THİS FUNCTİON
        logger.debug('Texlive için boxdims.sty kontrolü yapılıyor')
        if 'texlive' in list(conf['pdflatex-paths'].keys()):
            stdout, stderr = Popen('find / -wholename "*/texmf-dist/tex/latex" 2>&1 | grep -v "Permission denied" | grep -v "Invalid argument" | grep -v "No such file or directory"', shell = True, stdout = PIPE, stderr = PIPE).communicate()
            texlive_path = stdout.decode('utf-8').strip()
            if os.path.exists(texlive_path):
                commandwithpkexec = f'pkexec wget -P {texlive_path} https://mirrors.ctan.org/graphics/circuit_macros.zip && pkexec unzip {os.path.join(texlive_path, "circuit_macros.zip")} -d {texlive_path} && pkexec rm {os.path.join(texlive_path, "circuit_macros.zip")} && pkexec mv {os.path.join(texlive_path, "circuit_macros")} {os.path.join(texlive_path, "boxdims")}'
                commandasbash = f'wget -P {texlive_path} https://mirrors.ctan.org/graphics/circuit_macros.zip && unzip {os.path.join(texlive_path, "circuit_macros.zip")} -d {texlive_path} && rm {os.path.join(texlive_path, "circuit_macros.zip")} && mv {os.path.join(texlive_path, "circuit_macros")} {os.path.join(texlive_path, "boxdims")} && echo succesfull'
                
                if not os.path.exists(os.path.join(texlive_path, 'boxdims')):
                    if internet_connection():
                        stdout, stderr = Popen(f'pkexec bash -c "{commandasbash}"', shell = True, stdout = PIPE, stderr = PIPE).communicate()
                        
                        stdout = stdout.decode('utf-8').strip()
                        stderr = stderr.decode('utf-8').strip()
                        
                        if stdout.strip().endswith('succesfull'):
                            logger.info('Texlive: boxdims.sty başarılı bir şekilde indirildi')
                            result['texlive'] = True
                        else:
                            logger.error(f'stderr: {stderr}')
                            logger.error(f'stdout: {stdout}')
                            result['texlive'] = False
                    else:
                        result['texlive'] = False
                        logger.error('texlive: internet bağlantısı olmadığından boxdims.sty indirilemedi')
                else:
                    result['texlive'] = True
                    logger.info('Texlive: boxdims.sty zaten kurulu')
            else:
                result['texlive'] = False
                logger.error('Texlive: Texlive dizini bulunamadı')
    
    
    elif sys.platform == 'win32':
        logger.debug('Miktex için boxdims.sty kontrolü yapılıyor')
        if 'miktex' in list(conf['pdflatex-paths'].keys()):
            miktex_path = os.path.join(os.environ['LOCALAPPDATA'], 'Programs', 'MiKTeX', 'tex', 'latex', 'circuit_macros')
            if not os.path.exists(miktex_path):
                if internet_connection():
                    with open(miktex_path + '.zip', 'wb')as f:
                        f.write(requests.get('https://mirrors.ctan.org/graphics/circuit_macros.zip').content)
                    
                    print(Path(miktex_path).parent)
                    with zipfile.ZipFile(miktex_path + '.zip', 'r') as zip_ref:
                        zip_ref.extractall(Path(miktex_path).parent)
                        os.remove(miktex_path + '.zip')
                    if get_initexmf() != None:
                        Popen(f'{get_initexmf()} --update-fndb', shell=True, stdout = PIPE, stderr = PIPE).communicate()
                        logger.info('Miktex: boxdims.sty başarılı bir şekilde indirildi')
                        result['miktex'] = True
                    else:
                        logger.error('Miktex: initexmf bulunamadi')
                        result['miktex'] = False
                else:
                    result['miktex'] = False
                    logger.error('Miktex: internet bağlantısı olmadığından boxdims.sty indirilemedi')
            else:
                result['miktex'] = True
                logger.info('Miktex: boxdims.sty zaten kurulu')
        
        logger.debug('Texlive için boxdims.sty kontrolü yapılıyor')
        if 'texlive' in list(conf['pdflatex-paths'].keys()):
            stdout, stderr = Popen(r'dir C:\texlive\texmf-dist /s', shell = True, stdout = PIPE, stderr = PIPE).communicate()
            out = stdout.decode('utf-8').strip()
            texlive_path = os.path.join(out.split(' Directory of')[-1].split('\n')[0].strip(), 'texmf-dist', 'tex', 'latex')
            if os.path.exists(texlive_path):
                commandasbatch = f'curl -L -o {os.path.join(texlive_path, "circuit_macros.zip")} https://mirrors.ctan.org/graphics/circuit_macros.zip && unzip {os.path.join(texlive_path, "circuit_macros.zip")} -d {texlive_path} && del {os.path.join(texlive_path, "circuit_macros.zip")} && move {os.path.join(texlive_path, "circuit_macros")} {os.path.join(texlive_path, "circuit-macros")} && echo succesfull'

                if not os.path.exists(os.path.join(texlive_path, 'circuit-macros')):
                    if internet_connection():
                        stdout, stderr = Popen(f'{commandasbatch}', shell = True, stdout = PIPE, stderr = PIPE).communicate()
                        
                        stdout = stdout.decode('utf-8').strip()
                        stderr = stderr.decode('utf-8').strip()

                        if stdout.strip().endswith('succesfull'):
                            logger.info('Texlive: boxdims.sty başarılı bir şekilde indirildi')
                            result['texlive'] = True
                        else:
                            logger.error(f'stderr: {stderr}')
                            logger.error(f'stdout: {stdout}')
                            result['texlive'] = False
                    else:
                        result['texlive'] = False
                        logger.error('texlive: internet bağlantısı olmadığından boxdims.sty indirilemedi')
                else:
                    result['texlive'] = True
                    logger.info('Texlive: boxdims.sty zaten kurulu')
            else:
                result['texlive'] = False
                logger.error('Texlive: Texlive dizini bulunamadı')
    return result        


def get_initexmf():
    if sys.platform == 'linux':
        stdout, stderr = Popen('find / -name initexmf 2>&1 | grep -v "Permission denied" | grep -v "Invalid argument" | grep -v "No such file or directory"', shell = True, stdout = PIPE, stderr = PIPE).communicate()
        initexmf_path = stdout.decode('utf-8').strip()
    
    elif sys.platform == 'win32':
        stdout, stderr = Popen('where initexmf', shell = True, stdout = PIPE, stderr = PIPE).communicate()
        initexmf_path = stdout.decode('utf-8').strip()
    
    if initexmf_path:
        return initexmf_path
    else:
        return None


# this terminal code for find main miktex pdflatex path
"""

find / -name miktex-pdftex 2>&1 |
    grep -v "Permission denied" | grep -v "Invalid argument" | grep -v "No such file or directory"
    
"""




#miktex kütüphane yüklenme dizini

"""

/home/ozank/.miktex/texmfs/install/tex/latex/arabi/translit.sty

"""


# miktex database güncelleme komutu kullanımı
 
# öncelikle komutun yolunu bulmak için
"""

find / -name initexmf 2>&1 |
    grep -v "Permission denied" | grep -v "Invalid argument" | grep -v "No such file or directory"

"""

# çıkan komut dizinini kullanarak aşağıdaki komut uygulanır ve veritabanı güncellenir

"""

.../initexmf --update-fndb

"""




# this terminal code for all pdflatex path on main $PATH
# the output of this code can belong to any tex distro
"""

which pdflatex

"""




# Yukarıdaki kodlara ait çıktıları kontrol edeceğiz ve sonucunda hangi yolun hangi tex dağıtımına 
#   ait olduğunu tespit edeceğiz.


