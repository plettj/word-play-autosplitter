import argparse
import os
import socket
import time

LOG_FILE_TEMPLATE = (
    r"C:\Users\{username}\AppData\LocalLow\Game Maker's Toolkit\Word Play\Player.log"
)
HOST, PORT = "127.0.0.1", 16834
MAX_SPLITS = 10


def tail(filepath):
    with open(filepath, encoding="utf-8", errors="ignore") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line.strip()


def main():
    parser = argparse.ArgumentParser(
        description="AUTOSPLITTER - Word Play - Easy Mode.\n"
        "Make sure LiveSplit is open, and you've hit Control -> Start TCP Server."
        "Example usage:\n    wordplay_autosplitter.exe jlple"
    )
    parser.add_argument(
        "username",
        nargs="?",
        help="Your Windows username, for locating 'Player.log'",
    )
    args = parser.parse_args()

    if not args.username:
        args.username = input("Enter your Windows username (e.g., jlple): ").strip()

    log_path = LOG_FILE_TEMPLATE.format(username=args.username)

    if not os.path.isfile(log_path):
        print(f"[ERROR] Log file not found at:\n{log_path}")
        time.sleep(1)
        print("--- Closing Autosplitter ---")
        time.sleep(3)
        return

    print("[INFO] Connecting to LiveSplit Server...")
    try:
        sock = socket.create_connection((HOST, PORT))
    except Exception as e:
        print("[ERROR] Could not connect to LiveSplit Server:", e)
        time.sleep(1)
        print("--- Closing Autosplitter ---")
        time.sleep(3)
        return
    print("[INFO] Connected. Waiting for a game...")

    started = False
    split_count = 0

    for line in tail(log_path):
        if not started and "Picking seed" in line:
            sock.sendall(b"starttimer\r\n")
            started = True
            split_count = 0
            print("[INFO] Timer started.")

        elif started:
            if "shop" in line and split_count < MAX_SPLITS:
                sock.sendall(b"split\r\n")
                split_count += 1
                print(f"[INFO] Split {split_count}/{MAX_SPLITS}")

            if "Event,Type,Word" in line:
                if split_count < MAX_SPLITS - 1:
                    sock.sendall(b"reset\r\n")
                    print("[INFO] Run failed early.")
                else:
                    sock.sendall(b"split\r\n")
                    print("[INFO] Final split sent; run completed.")
                print("[INFO] Waiting for a new game...")
                started = False
                split_count = 0


if __name__ == "__main__":
    main()
