import socket
import threading
import time

tLock = threading.Lock()

host = '127.0.0.1'
port = 5000

clients = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)
arquivo = open('conversa.txt', 'r')
conteudo = arquivo.readlines()

quitting = False
print("Server Started.")
while not quitting:
    try:
        data, addr = s.recvfrom(1024)
        decoded_data = data.decode('utf-8')
        tLock.acquire()
        conteudo.append(decoded_data +'\n')
        arquivo = open('conversa.txt', 'w')
        arquivo.writelines(conteudo)
        arquivo.close()
        tLock.release()
        if ("Quit") in str(decoded_data):
            quitting = True

        if addr not in clients:
            print("Client ", addr, "has connected.")
            clients.append(addr)

        #data_message,date_message = decoded_data.split('|',1)
        #if(time.ctime(time.time()) > decoded_data.split("|")[1])
        print(time.ctime(time.time()))
        #else
        #print(date_message)
        print(addr, ":", decoded_data.split("\n")[0])
        time.sleep(0.2)
        for client in clients:
            if addr != client:
                s.sendto(data, client)

    except:
        pass
s.close()
