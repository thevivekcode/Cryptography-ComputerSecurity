
# coding: utf-8

# In[ ]:


import socket
import time
# In[ ]:

def keepAlive(type,payload, size):
    if type == 1:  #request
        data  = "$" + payload +"$" +str(size)
        return data
    else: #response
        return "OK running and alive"


def client_connection():
    host = socket.gethostname()  # as both code is running on same pc
    port = 1234  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    print("Attacker is now connected to server\n")
    print("Attacker will use KEEPALIVE/HEARTBEAT to perform a HEARTBLEED ATTACK\n")
    print("Enter size to perform heartbleed from server cache\n")
    print("Make sure it is greater than actual payload lenght i.e > 5\n")
    message = "Hello"
    while message.lower().strip() != 'bye':

        message = input(" -> ")  # again take input

        if(message.lower().strip() != "bye"):
            keepAliveMssg = keepAlive(1,"alive",int(message))
            client_socket.send(keepAliveMssg.encode())  # send keepAlive request
            response = client_socket.recv(1024).decode()  # receive response
            print('heartbeat response from server ==> ' + response)  # show in terminal
            print("\n")




    client_socket.close()  # close the connection


if __name__ == '__main__':

    client_connection()
