
import socket
'''
  Cache is the memory part where we exploit the vulnerability of OpenSSL .
  Since in OpenSSL v 1.01 it copies all the data from memory of specific size
  mentioned in heartbeat_request.
  This results in major flaw if cache contains important info.
'''
cache = ""


def isalive(data):
    if data[0]=="$":
        return True
    return False

def heartbeat_response(data):
    global cache
    data_list = data.split('$')[1:]
    payload = data_list[0]
    size = int(data_list[1])
    pointer  = cache.find(payload)
    return cache[pointer:pointer+size]



def server_connection():
    global cache
    host = socket.gethostname()
    port = 1234  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    while True:
        conn, address = server_socket.accept()  # accept new connection
        print("\n")
        print("Connection from: " + str(address))
        while True:
            data = conn.recv(1024).decode()
            cache  += " " + str(data)
            if not data:# if data is not received break
                break



            if isalive(data):
                print("HEARTBEAT req from client received: " + str(data)[1:-2])
                response_data = heartbeat_response(data)
            else:
                print("from connected user: " + str(data))
                response_data = "OK"


            conn.send(response_data.encode())  # send data to the client

        conn.close()  # close the connection


if __name__ == '__main__':
    print("Welcome to server\n")
    print("All request and response generated are protected using simulation based OpenSSL\n")
    print("Simulation is based on HEARTBLEED Bug which is a serious vulnerability in the popular OpenSSL\n")

    server_connection()
