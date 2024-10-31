# file_sharing/file_transfer.py

import socket
import os

CHUNK_SIZE = 4096

async def send_file(peer_ip, file_data):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((peer_ip, 5000))
        sock.sendall(file_data.encode())
        sock.close()
        return True
    except:
        return False