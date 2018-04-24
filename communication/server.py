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
arquivo = open('conversa.txt', 'w+')
conteudo = arquivo.readlines()

quitting = False
print("Server Started at port:", port, "and address:", host, ".")
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
            print("Client", addr, "has connected as", decoded_data.split(' ')[0].replace(":", ""), "at", time.ctime(time.time()))
            clients.append(addr)
        else:
            m = decoded_data.split(' ')
            for i, token in enumerate(m[:]):
                if token == 'Date:':
                    break
            data = m[i+4:i+5]
            #print(data)
            data = str(data).replace(":", " ").replace("[", "").replace("]", "").replace("\'", "")
            data = data.split(' ')
            segundos_cliente = (int(data[0]))*60*60 + (int(data[1]))*60 + (int(data[2])) #segundos da mensagem do cliente quando chega no servidor
            print(segundos_cliente)

            segundos_servidor = time.ctime(time.time())
            segundos_servidor = (segundos_servidor).split(' ')[3:4]
            segundos_servidor = str(segundos_servidor).replace(":", " ").replace("[", "").replace("]", "").replace("\'", "")
            segundos_servidor = segundos_servidor.split(' ')
            segundos_servidor = (int(segundos_servidor[0]))*60*60 + (int(segundos_servidor[1]))*60 + (int(segundos_servidor[2])) #segundos do servidor quando chega a mensagem do cliente

            print(segundos_servidor)


            print(time.ctime(time.time()), "|", decoded_data.split("\n")[0])
            for client in clients:
                if addr != client:
                    s.sendto(data, client)
    except:
        pass
s.close()
