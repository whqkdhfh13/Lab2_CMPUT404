import socket


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 8080  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect(("127.0.0.1", port))  # connect to the server

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(4096).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()