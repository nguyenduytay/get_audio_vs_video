import win32inet  # pywin32
import win32inetcon

def wininet_example():
    # Initialize WinInet
    hInternet = win32inet.InternetOpen(
        "MyAgent/1.0",
        win32inetcon.INTERNET_OPEN_TYPE_DIRECT,
        None,
        None,
        0
    )
    
    # Open URL
    hUrl = win32inet.InternetOpenUrl(
        hInternet,
        "https://api.example.com/data",
        None,
        0,
        win32inetcon.INTERNET_FLAG_RELOAD,
        0
    )
    
    # Read data
    data = bytearray()
    while True:
        buffer = win32inet.InternetReadFile(hUrl, 4096)
        if not buffer:
            break
        data.extend(buffer)
    
    # Cleanup
    win32inet.InternetCloseHandle(hUrl)
    win32inet.InternetCloseHandle(hInternet)
    
    return bytes(data)