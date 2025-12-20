import os
from cryptography.fernet import Fernet

# Khóa bí mật (Cần được bảo mật kỹ)
# key = Fernet.generate_key() 
key = b'9H1NDZk0NFkGpmlbB6r4bWwB3rPbXvirbW-w9cUnBBg='
fernet = Fernet(key)

def encrypt_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        encrypted = fernet.encrypt(data)
        with open(file_path, 'wb') as f:
            f.write(encrypted)
        print(f"Đã mã hóa: {file_path}")
    except Exception as e:
        print(f"Lỗi khi mã hóa {file_path}: {e}")

def decrypt_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        decrypted = fernet.decrypt(data)
        with open(file_path, 'wb') as f:
            f.write(decrypted)
        print(f"Đã giải mã: {file_path}")
    except Exception as e:
        print(f"Lỗi khi giải mã {file_path}: {e}")

def process_directory(directory_path, mode='encrypt'):
    if not os.path.exists(directory_path):
        print(f"Thư mục không tồn tại: {directory_path}")
        return

    print(f"Bắt đầu {mode} thư mục: {directory_path}")
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            if mode == 'encrypt':
                encrypt_file(file_path)
            elif mode == 'decrypt':
                decrypt_file(file_path)

if __name__ == "__main__":
    # Đường dẫn thư mục cần xử lý
    tests_path = r"D:\hoc web\get_audio_vs_video\tests"
    
    # Chế độ mặc định: 'encrypt' (mã hóa)
    # Thay đổi thành 'decrypt' khi muốn giải mã
    target_mode = 'decrypt' 
    
    process_directory(tests_path, mode=target_mode)