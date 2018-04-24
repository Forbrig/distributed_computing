import socket
import threading
import time

tLock = threading.Lock()
shutdown = False

def receving(name, sock):
    while not shutdown:
        try:
            tLock.acquire()
            while True:
                data, addr = sock.recvfrom(1024)
                decoded_data = data.decode('utf-8')
                print(decoded_data)
        except:
            pass
        finally:
            tLock.release()

# def past_conv():
#     arquivo = open('conversa.txt', 'r')
#     conteudo = arquivo.readlines()
#     print(conteudo)


host = '127.0.0.1'
port = 0

server = ('127.0.0.1', 5000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

receivingThread = threading.Thread(target = receving, args = ("RecvThread", s))
receivingThread.start()

#past_conv()
#messages = []
print("Press enter to send the message.")
alias = input("Name: ")
message = alias
message = message.encode('utf-8')
# connect message
s.sendto(message, server)

message = input()
#messages.append(message)

while (message != 'Quit'):
    if (message != ''):
        message = (alias + ": " + message + " Date: " + time.ctime(time.time()))
        #print(message)
        message = message.encode('utf-8')

        time.sleep(2)
        s.sendto(message, server)
    message = input()
    #time.sleep(0.3)

message = 'Desconnecting from server'
message = (alias + ": " + message)
message = message.encode('utf-8')
s.sendto(message, server)
shutdown = True
receivingThread.join()
s.close()
