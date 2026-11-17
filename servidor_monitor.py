import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 9000
TIMEOUT_OFFLINE = 8
CHECK_INTERVAL = 1

last_seen = {}
lock = threading.Lock()

def handle_client(conn):
    try:
        data = conn.recv(1024).decode().strip()
        if data.startswith("PING"):
            parts = data.split()
            node_id = parts[1] if len(parts) > 1 else "unknown"
            with lock:
                last_seen[node_id] = time.time()
    finally:
        conn.close()

def accept_loop(sock):
    while True:
        conn, _ = sock.accept()
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

def checker_loop():
    alerted = set()
    while True:
        now = time.time()
        with lock:
            for node_id, ts in list(last_seen.items()):
                if now - ts > TIMEOUT_OFFLINE:
                    if node_id not in alerted:
                        print(f"[ALERTA] O N\u00f3 {node_id} est\u00e1 OFFLINE!", flush=True)
                        alerted.add(node_id)
                else:
                    alerted.discard(node_id)
        time.sleep(CHECK_INTERVAL)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen()
    print(f"Servidor Monitor ouvindo em {HOST}:{PORT}")
    threading.Thread(target=accept_loop, args=(sock,), daemon=True).start()
    checker_loop()

if __name__ == "__main__":
    main()
