from sys import platform
from pathlib import Path
from json import load, dump
from datetime import datetime
import logging, os
from logging.handlers import RotatingFileHandler

def writeConf(data):
    if platform == 'win32':
        with open(str(Path(__file__).parent.parent)+'\\configurations.json', 'w', encoding='utf-8')as f:
            dump(data, f, indent=2, ensure_ascii=False)
    elif platform == 'linux':
        with open(str(Path(__file__).parent.parent)+'/configurations.json', 'w', encoding='utf-8')as f:
            dump(data, f, indent=2, ensure_ascii=False)
    return data
def readConf():
    if platform != 'linux':
        with open(str(Path(__file__).parent.parent)+'\\configurations.json', encoding='utf-8')as f:
            return load(f)
    else:
        with open(str(Path(__file__).parent.parent)+'/configurations.json', encoding='utf-8')as f:
            return load(f)

def setup_logging():
    log_directory = 'logs'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    date_str = datetime.now().strftime('%Y-%m-%d')
    log_filename = os.path.join(log_directory, f'{date_str}.log')

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Remove existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = RotatingFileHandler(log_filename, maxBytes=5*1024*1024, backupCount=5)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


"""
def setup_logging():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler("app.log"),
                            logging.StreamHandler()
                        ])
"""