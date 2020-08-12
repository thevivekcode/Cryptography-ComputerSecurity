
# coding: utf-8

# In[ ]:


import socket
import threading
from _thread import *
import time
# In[ ]:

def keepAlive(type,payload, size):
    if type == 1:  #request
        data  = "$" + payload +"$" +str(size)
        return data
    else: #response
        return "OK running and alive"


def heartbeat(client_socket):
    keepAliveMssg = keepAlive(1,"alive",5)
    try:
        client_socket.send(keepAliveMssg.encode())  # send keepAlive request
        response = client_socket.recv(1024).decode()
        threading.Timer(10.0, heartbeat, args = (client_socket,)).start()
    except:
        exit()

def client_connection():
    host = socket.gethostname()  # as both code is running on same pc
    port = 1234  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    print("Client is now connected to server using simulation based openSSL\n")
    print("OpenSSL provides secure communications over computer networks against eavesdropping.\n")
    print("Cleint will automatically send a HEARTBEAT req to server every few seconds \n")

    message = "Hello"
    # curr_time = time.time()
    threading.Timer(10.0, heartbeat, args = (client_socket,)).start()
    # heartbeat(client_socket)
    while message.lower().strip() != 'bye':

        message = input(" -> ")  # again take input
        client_socket.send(message.encode())  # send message
        response = client_socket.recv(1024).decode()  # receive response
        print('Received from server: ' + response)

        # # it checks after every 6 sec if the sever connection is still secure and alive
        # if(time.time()- curr_time > 6):
        #     keepAliveMssg = keepAlive(1,"alive",5)
        #     client_socket.send(keepAliveMssg.encode())  # send keepAlive request
        #     response = client_socket.recv(1024).decode()  # receive response
        #     print('HEARTBEAT response from server: ' + response)  # show in terminal
        #     curr_time = time.time()



    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_connection()
