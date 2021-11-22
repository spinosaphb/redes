from socket import *
import sys 
import json

target_host = "localhost" 
target_port = 3333

with socket(AF_INET, SOCK_STREAM) as sock:

    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((target_host, target_port))
    sock.listen(1)

    try:
        while True:
            conn, addr = sock.accept()
            message = conn.recv(1024).decode()
            # Redirecionar as rotas
            filename = message.split()[1][1:]
            filename = 'index.html' if filename == '' else filename
            pages = ['index.html','notas.html','redes.html']

            if filename in pages:
                conn.send('HTTP/1.0 200 OK\r\n'.encode('utf-8'))
                conn.send("Content-Type: text/html\r\n".encode('utf-8'))
                with open(filename, 'r') as file:
                    outputdata = file.readlines() 
                
                for item in outputdata:
                    conn.send(item.encode('utf-8'))
                    conn.send("\r\n".encode('utf-8'))
                
            else:
                conn.send('HTTP/1.0 404 NotFound\r\n'.encode('utf-8'))
                conn.send("Content-Type: text/html\r\n".encode('utf-8'))               
                conn.send('<html><body><h1>PageNotFound</body></html>'.encode('utf-8'))
                raise FileNotFoundError('Arquivo não encontrada')

            conn.close()

    except Exception as e:
        print(e)
