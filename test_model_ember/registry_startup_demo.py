import winreg  # Python's built-in registry module

# Example: Add to startup
def add_to_startup():
    key = winreg.HKEY_CURRENT_USER
    subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    try:
        # Open registry key
        registry_key = winreg.OpenKey(key, subkey, 0, winreg.KEY_WRITE)
        
        # Set value
        winreg.SetValueEx(registry_key, "MyApp", 0, winreg.REG_SZ, 
                         r"C:\path\to\your\app.exe")
        
        winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False

# More advanced registry operations
def advanced_registry_ops():
    # Create key
    key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, 
                          r"SYSTEM\CurrentControlSet\Services\MyService")
    
    # Set multiple values
    winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, "My Service")
    winreg.SetValueEx(key, "ImagePath", 0, winreg.REG_EXPAND_SZ, 
                     r"%SystemRoot%\system32\svchost.exe -k myservice")
    winreg.SetValueEx(key, "Start", 0, winreg.REG_DWORD, 2)  # Auto-start
    
    winreg.CloseKey(key)