import socket

def internet_connection():
    try:
        print("İnternet bağlantısı kontrol ediliyor")
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except (OSError, socket.timeout):
        return False


