import sys
import time
from socket import *

DEF_HOST = '127.0.0.1'
DEF_PORT = 12000
TIMEOUT_SEC = 1.0
NUM_PINGS = 10

def main():
    # Parse optional host/port from command line
    host = DEF_HOST
    port = DEF_PORT
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])

    clientSocket = socket(AF_INET, SOCK_DGRAM) # Create a UDP socket

    clientSocket.settimeout(TIMEOUT_SEC) # Set socket timeout so recvfrom() won't block forever

    if sys.platform.startswith("win"):
        try:
            import socket as _s
            clientSocket.ioctl(_s.SIO_UDP_CONNRESET, False) 
        except Exception:
            # Some Python/Windows versions need a bytes arg; try a fallback.
            try:
                import struct
                clientSocket.ioctl(getattr(_s, "SIO_UDP_CONNRESET", 0x9800000C),
                                struct.pack("I", 0))
            except Exception:
                pass # If not supported just continue.

    sent = 0
    received = 0
    rtts = []  # store successful RTTs for stats

    print(f'Sending {NUM_PINGS} UDP pings to {host}:{port} ...')
    for seq in range(1, NUM_PINGS + 1):
        send_time = time.time()
        message = f'Ping {seq} {send_time}'.encode('ascii')

        clientSocket.sendto(message, (host, port))
        sent += 1

        try:
            t0 = time.time()
            data, addr = clientSocket.recvfrom(1024)
            t1 = time.time()

            rtt = t1 - t0
            received += 1
            rtts.append(rtt)

            print(f'Reply from {addr[0]}:{addr[1]}: {data.decode("ascii", errors="replace")} '
                  f'RTT={rtt:.6f}s')

        except (timeout, ConnectionResetError):
            print('Request timed out')

    # Print summary statistics
    loss = ((sent - received) / sent) * 100.0
    print('\n---- Ping statistics ----')
    print(f'{sent} packets transmitted, {received} received, {loss:.1f}% packet loss')
    if rtts:
        rtt_min = min(rtts)
        rtt_avg = sum(rtts)/len(rtts)
        rtt_max = max(rtts)
        print(f'RTT min/avg/max = {rtt_min:.6f}/{rtt_avg:.6f}/{rtt_max:.6f} seconds')

    clientSocket.close()

if __name__ == '__main__':
    main()
