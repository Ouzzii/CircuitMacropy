import socket, logging
from modules.configuration_utils import setup_logging
setup_logging()
logger = logging.getLogger(__name__)

def internet_connection():
    try:
        logger.debug("İnternet bağlantısı kontrol ediliyor")
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except (OSError, socket.timeout):
        return False


