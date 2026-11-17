import socket
import sys
import time

HOST = "127.0.0.1"
PORT = 9000
INTERVAL = 3

def main():
    node_id = sys.argv[1] if len(sys.argv) > 1 else "Worker_1"
    while True:
        try:
            with socket.create_connection((HOST, PORT), timeout=2) as sock:
                sock.sendall(f"PING {node_id}".encode())
        except Exception as e:
            print(f"Erro ao enviar heartbeat: {e}", flush=True)
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
