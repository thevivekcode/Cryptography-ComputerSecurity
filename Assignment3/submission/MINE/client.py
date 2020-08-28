import socket
import threading
import sys
from _thread import *

t = []

def keepAlive(type,payload, size):
    data  = "$" + payload +"$" +str(size)
    return data


def heartbeat(client_socket):
    global t
    keepAliveMssg = keepAlive(1,"alive",5)
    try:
        client_socket.send(keepAliveMssg.encode())  # send keepAlive request
        response = client_socket.recv(1024).decode()
        t.append(threading.Timer(12.0, heartbeat, args = (client_socket,)).start())
    except:
        exit()

def sendHello(client_socket):
    message = "Hello"
    print("Client Sending Hello to Server")
    client_socket.send(message.encode())  # send message

def waitForServerHello(client_socket):
    response = client_socket.recv(1024).decode()  # receive response
    print('Received from server: ' + response)

def getServerCertificates(client_socket):
    response = client_socket.recv(1024).decode()  # receive response
    decrypt
    print("Certificates from server recieved")

def sendCertificatesToServer(client_socket):

    client_socket.send(certi.encode())  # send message

def sendFinalAck(client_socket):
    message = "Acknowledged : TRUE"
    print("Client Sending final Acknowledgement to Server")
    client_socket.send(message.encode())  # send message

def receiveFinalAck(client_socket):
    response = client_socket.recv(1024).decode()  # receive response
    print('Received from server: ' + response)

def handshaking(client_socket):
    sendHello(client_socket)
    waitForServerHello(client_socket)
    sendFinalAck(client_socket)
    receiveFinalAck(client_socket)


def client_connection():
    global t
    host = socket.gethostname()  # as both code is running on same pc
    port = 1235  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    print("OpenSSL provides secure communications over computer networks against eavesdropping.\n")
    print("Cleint will automatically send a HEARTBEAT req to server every few seconds \n")

    #Handshaking ------------------------------------------------------------------------------
    print("ATTEMPTING HANDSHAKING WITH SERVER\n")
    print("****************************************************")
    handshaking(client_socket)
    print("\nConnected to Server")
    print("****************************************************\n")
    print("Cleint and Server agreed to use OpenSSL v1.01")
    print('---------------------------------------\n')
    #-------------------------------------------------------------------------------------------

    message = "Hello"

    # REGULAR HEARTBEAT BY CLIENT *************************************
    # t.append(threading.Timer(12.0, heartbeat, args = (client_socket,)).start())
    #******************************************************************


    print("To close connection enter --> BYE")
    print("To initiate HEARTBLEED MODE enter --> ATTACK\n")
    while message.lower().strip() != 'attack': # if attack is called initiate HEARTBLEED attack
        message = input(" -> ")  # again take input
        if message.lower().strip() == "bye":
            client_socket.close()  # close the connection
            sys.exit(1)
            return
        client_socket.send(message.encode())  # send message
        response = client_socket.recv(1024).decode()  # receive response
        print('Received from server: ' + response)

    while message:
        message = input("\n enter payload message -> ")  # again take input
        if message.lower().strip() == "bye":
            client_socket.close()  # close the connection
            sys.exit(1)
            return
        size = input(" enter payload size INTEGER -> ")
        heartbleed_attack = keepAlive(1, message, size)
        client_socket.send(heartbleed_attack.encode())  # send message
        response = client_socket.recv(1024).decode()  # receive response
        print("\nHEARTBLEED RESPONSE FROM SERVER \n")
        print(" ".join(hex(ord(n)) for n in response), "\t\t",response)




if __name__ == '__main__':

    client_connection()
    sys.exit()
