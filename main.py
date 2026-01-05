from MyDB.main import*
import socket
import threading
import datetime
from protocol.protocol import *
from MyDB.errors import*

def handle_client_commands(client, address):
    print(f"working on: {address}")

    username = recv(client)[1]
    password = recv(client)[1]
    database = recv(client)[1]
    command = recv(client)[1]
    if command.strip().startswith("/"):
        try:
            result = program_command(username, password, command)
        except DBMSErrors as e:
            send_text(client, str(e))
            return None
    else:
        try:
            result = sql_command(username, password, database, command)
        except DataBaseError as e:
            send_error(client, str(e))
            return None
    if "SELECT" in command:
        send_file(client, result, "JSN")
    else:
        send_text(client, result)


HOST = "0.0.0.0"
#HOST = "127.0.0.1"
PORT = 10011

socket_test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket_test.bind((HOST, PORT))
socket_test.listen(1)

users = []
print("server working")
try :
    while True:
        info = socket_test.accept()
        socket_client = info[0]
        address = info[1]

        thread = threading.Thread(target = handle_client_commands, args=[socket_client, address])

        thread.start()

except KeyboardInterrupt:
    print("closing")

finally:
    socket_test.close()