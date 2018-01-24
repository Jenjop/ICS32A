import socket

#Connect to Server
def connect(host: str, port: int) -> 'connection':

    ##Create socket and connect to given server
    connection_socket = socket.socket()
    connection_socket.connect((host,port))

    ##Create read and write sockets
    connection_socket_in = connection_socket.makefile('r')
    connection_socket_out = connection_socket.makefile('w')

    print('Connected')

    return connection_socket, connection_socket_in, connection_socket_out

#Close Connection to Server
def close(connection: 'connection') -> None:

    connection_socket, connection_socket_in, connection_socket_out = connection

    connection_socket_in.close()
    connection_socket_out.close()
    connection_socket.close()

#Send Message
def send_message(connection: 'connection', message: str) -> None:
     connection_socket, connection_socket_in, connection_socket_out = connection

     connection_socket_out.write(message + '\r\n')
     connection_socket_out.flush()

#Receive Response
def receive_response(connection: 'connection') -> None:
    connection_socket, connection_socket_in, connection_socket_out = connection

    return connection_socket_in.readline()[:-1]

#Send Message and Listen for Response
def send_receive(connection: 'connection', message: str) -> None:
    connection_socket, connection_socket_in, connection_socket_out = connection

    connection_socket_out.write(message + '\r\n')
    connection_socket_out.flush()


    return connection_socket_in.readline()[:-1]
