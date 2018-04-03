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

host = '127.0.0.1'
port = 0

server = ('127.0.0.1', 5000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

receivingThread = threading.Thread(target = receving, args = ("RecvThread", s))
receivingThread.start()

alias = input("Name: ")
message = input(alias + "-> ")
while (message != 'Quit'):
    if (message != ''):
        message = (alias + ": " + message)
        message = message.encode('utf-8')
        s.sendto(message, server)
    tLock.acquire()
    message = input(alias + "-> ")
    tLock.release()
    time.sleep(0.2)

shudown = True
receivingThread.join()
s.close()
