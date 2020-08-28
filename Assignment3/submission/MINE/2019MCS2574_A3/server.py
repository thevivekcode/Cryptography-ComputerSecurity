

import socket
'''
  Cache is the memory part where we exploit the vulnerability of OpenSSL .
  Since in OpenSSL v 1.01 it copies all the data from memory of specific size
  mentioned in heartbeat_request.
  This results in major flaw if cache contains important info.
'''
cache = "Security_lev:auth_keys4jdf%{h)ndf...login&pass:secretpass,"


def heartBleed(mssg,size):
    mssglen = abs(size - len(mssg))
    if mssglen == 0:
        return ""
    return cache[-mssglen:]

def receiveHello(conn):
    data = conn.recv(1024).decode()
    print('Received from Client: ' + data)

def sendHello(conn):
    print("Sending Hello to Client")
    message = "Hello"
    conn.send(message.encode())

def receiveACK(conn):
    data = conn.recv(1024).decode()
    print('Received from Client: ' + data)

def sendACK(conn):
    print("Sending Acknowledged : TRUE to Client")
    message = "Acknowledged : TRUE"
    conn.send(message.encode())

def handshake(conn, address):
    receiveHello(conn)
    sendHello(conn)
    receiveACK(conn)
    sendACK(conn)

def client(conn, address):
    global cache
    print("Server in HANDSHAKING MODE \n")
    print("****************************************************")
    handshake(conn, address)
    print("Connection from: " + str(address))
    print("****************************************************\n")
    mode = 'normal'
    while True:

        if mode =='attack':
            data = conn.recv(1024).decode()
            dataList = data.split("$")[1:]
            if len(dataList) < 2:
                break
            mssg = dataList[0]
            size = int(dataList[1])
            print("Received Heartbead req: "+mssg +" " +str(size) )
            response_data = heartBleed(mssg,size)
            conn.send(response_data.encode())
            continue

        data = conn.recv(1024).decode()


        if not data:  # if data is not received return and close the connection
            return

        if data=='bye': # close connection
            return

        if data.lower().strip()=='attack': # HEARTBLEED ATTACK MODE
            mode =  'attack'
            conn.send("hearbeat requested".encode())  # send data to the client
            continue



        if len(data) > 0 and data[0]=='$': # heartbeat message
            response_data = "HEARTBEAT Request received from Client"
            conn.send(response_data.encode())  # send data to the client
            print("from connected user: " + str(response_data))
        else:
            cache  += " " + str(data) # if normal communication save in server cache
            response_data = "OK"
            print("from connected user: " + str(data))
            conn.send(response_data.encode())  # send data to the client

def server_connection():
    global cache
    host = socket.gethostname()
    port = 1235  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind host address and port together
    server_socket.listen(3)   # configure how many client the server can listen simultaneously

    while True:
        conn, address = server_socket.accept()  # accept new connection
        client(conn, address)
        conn.close()  # close the connection



if __name__ == '__main__':
    print("Welcome to server")
    print("Simulation is based on HEARTBLEED Bug which is a serious vulnerability in the popular OpenSSL\n")

    server_connection()
