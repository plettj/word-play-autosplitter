import socket
import time

# cd C:/Users/jlple/Documents/Miscellaneous/Gaming/wordplay

# pyinstaller --onefile --name logwatch basic_autosplitter_easy_mode.py

LOG_PATH = r"C:\Users\jlple\AppData\LocalLow\Game Maker's Toolkit\Word Play\Player.log"
HOST, PORT = "127.0.0.1", 16834


def tail(f):
    f.seek(0, 2)
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.1)
            continue
        print("[LOG]", line.strip())
        yield line.strip()


def main():
    print("[INFO] Connecting to LiveSplit Server...")
    sock = socket.create_connection((HOST, PORT))
    print("[INFO] Connected.")

    def send(cmd):
        print("[SEND]", cmd)
        try:
            sock.sendall((cmd + "\r\n").encode())
        except Exception as e:
            print("[ERROR] Failed to send command:", e)

    print("[INFO] Waiting for start...")

    started = False
    split_count = 0
    max_splits = 10

    for line in tail(open(LOG_PATH, encoding="utf-8", errors="ignore")):
        if not started and "Picking seed" in line:
            send("starttimer")
            started = True
            split_count = 0

        elif started:
            # Handle round splits
            if "shop" in line:
                if split_count < max_splits:
                    send("split")
                    split_count += 1
                    print(f"[INFO] Split {split_count}/{max_splits}")

            # Handle end of run
            if "Event,Type,Word" in line:
                send("split")  # Final split at end of run, finishes the run!
                print("[INFO] Run ended.")
                started = False
                split_count = 0


if __name__ == "__main__":
    main()
