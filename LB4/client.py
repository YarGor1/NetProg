# Echo client program
import socket, os

HOST = '127.0.0.1'          # The remote host
PORT = 50007                # The same port as used by the server
file = 'tasks.txt'          # filename
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    with open(file, 'rb') as f:
        file_size = str(os.path.getsize(file)).encode('utf-8') # Розмір файлу
        file_size = file_size.zfill(8) # Дозаповнення до 8 байт
        s.sendall(file_size)           # Відправка розміру файлу 
        print(f"Початок відправки файлу: {file}")
        bytes_sent = s.sendfile(f)     # Відправка файлу
        print(f"Успішно відправлено: {bytes_sent} байтів.")


