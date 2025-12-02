import socket, os

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
nmbr = 0                # Номер файлу

while True:             # Постійне функціонування серверу
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        
        with conn:
            print('Connected by', addr)
            while True:
                try:
                    fsize = int(str(conn.recv(8).decode('utf-8'))) # Отримання фіксованого розміру файлу

                    with open(f'file_{nmbr}.txt', 'wb') as f:   # Створення і запис у файл
                        f.write(conn.recv(fsize))
                        print(f'file_{nmbr}.txt is Done')                        
                        nmbr += 1

                    if not fsize: break
                    break
                
                except (ConnectionAbortedError, ConnectionResetError):  # Обробка помилок
                    break

                    
