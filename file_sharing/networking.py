# file_sharing/networking.py

import socket
import threading

async def discover_peers():
    # This is a simplified version. In a real-world scenario, you'd use a more
    # sophisticated method like UPnP or a centralized server for peer discovery.
    peers = []
    for i in range(1, 255):
        ip = f"192.168.1.{i}"
        if ip != await get_local_ip():
            if await is_port_open(ip, 5000):
                peers.append(ip)
    return peers

async def connect_to_peer(peer_ip):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((peer_ip, 5000))
        sock.close()
        return True
    except:
        return False

async def receive_connection(peer_ip, accept):
    try:
        if accept:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('', 5000))
            sock.listen(1)
            conn, _ = sock.accept()
            # Handle file transfer here
            conn.close()
            sock.close()
        return True
    except:
        return False

async def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip

async def is_port_open(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.1)
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0