import socket
from threading import Thread

BYTES_TO_READ = 4096
PROXY_SERVER_HOST = "127.0.0.1"
PROXY_SERVER_PORT = 8080

def send_back(host, port, request):
    
    with socket.socket() as cs:
        cs.connect((host, port))
        cs.send(request)
        cs.shutdown(socket.SHUT_WR)
        
        res = b''
        data = cs.recv(BYTES_TO_READ)
        
        while len(data) > 0:
            res += data
            data = cs.recv(BYTES_TO_READ)
            
        return res
    
def handle_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")

        request = b''
        while True:
            data = conn.recv(BYTES_TO_READ) 
            if not data:
                break
            request += data
        response = send_back("www.google.com", 80, request) 
        conn.sendall(response)
        
        
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss:
        ss.bind((PROXY_SERVER_HOST,PROXY_SERVER_PORT))
        ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        conn, addr = ss.accept()

        handle_connection(conn, addr)


def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss:
        ss.bind((PROXY_SERVER_HOST,PROXY_SERVER_PORT))
        ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        while True:
            conn, addr = ss.accept()
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()



start_threaded_server()
