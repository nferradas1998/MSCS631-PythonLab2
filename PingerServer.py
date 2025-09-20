import random
from socket import *

def main():
    # Create a UDP socket (SOCK_DGRAM)
    serverSocket = socket(AF_INET, SOCK_DGRAM)

    # Bind to all interfaces on UDP port 12000
    serverSocket.bind(('', 12000))
    print('UDP Ping Server listening on 0.0.0.0:12000 (Ctrl+C to stop)')

    while True:
        # Generate random number in the range [0, 10]
        rand = random.randint(0, 10)

        # Receive the client packet along with the address it is coming from
        message, address = serverSocket.recvfrom(1024)

        # Capitalize the message from the client
        message = message.upper()

        # If rand is less than 4, we consider the packet lost and do not respond
        if rand < 4:
            # Simulate packet loss by not replying
            continue

        # Otherwise, the server responds
        serverSocket.sendto(message, address)

if __name__ == '__main__':
    main()
