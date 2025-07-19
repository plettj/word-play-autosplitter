import socket

try:
    with socket.create_connection(("127.0.0.1", 16834)) as sock:
        sock.sendall(b"starttimer\n")
        print("✅ Command sent successfully")
except Exception as e:
    print("❌ Failed to connect/send:", e)
