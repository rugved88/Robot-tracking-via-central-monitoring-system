import socket
import time
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

local_hostname = socket.gethostname()
local_fqdn = socket.getfqdn()

ip_address = socket.gethostbyname(local_hostname)
port = 55469

server_address = (ip_address, port)

# print (f"Working on {local_hostname} ({local_fqdn}) with {ip_address}")
time.sleep(1)
print("Starting server-side connection: ")
# print (f"\tIP Address {ip_address} ")
# print (f"\tPort: {port} ")
time.sleep(1)

sock.bind(server_address)
sock.listen(1)
timeout = 0


def acceptConnection():
    while True:
        print("Waiting for a connection from client-side.")
        connection, client_address = sock.accept()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            print("Received connection from client.")
            # print ('Connection from', client_address)

            while True:
                data = connection.recv(64)
                if data:
                    print(f"Received data: {data} ")
                    data1 = data
                else:
                    print("\nThere is no more data to receive.")
                    break

        finally:
            connection.close()
            print("nConnection closed.")
            return data1
            # exit()

    print("cont")


acceptConnection()
