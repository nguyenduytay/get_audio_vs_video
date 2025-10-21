# Multi-Utility Dashboard

Dashboard đa chức năng với khả năng mở rộng, được thiết kế để dễ dàng thêm các tiện ích mới.

## 🏗️ Cấu trúc dự án

```
Multi-Utility-Dashboard/
├── main_dashboard.py          # Dashboard chính
├── modules/                   # Thư mục chứa các modules
│   ├── __init__.py
│   └── video_downloader.py    # Module tải video
├── build_exe.py              # Script build .exe
├── build_exe.bat             # Batch build script
├── requirements.txt           # Dependencies
└── README_DASHBOARD.md        # Hướng dẫn này
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

## 🔧 Cách phát triển

### Thêm module mới:

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

## 📦 Build và phân phối

### Cài đặt dependencies:

```bash
pip install -r requirements.txt
```

### Build file .exe:

```bash
# Cách 1: Sử dụng batch script
build_exe.bat

# Cách 2: Chạy Python trực tiếp
python build_exe.py
```

### Kết quả:

- `dist/MultiUtilityDashboard.exe` - File thực thi chính
- `dist/installer/` - Gói cài đặt cho người dùng

## 🎯 Lợi ích của cấu trúc mới

### ✅ **Mở rộng dễ dàng:**

- Thêm module mới chỉ cần tạo file trong `modules/`
- Dashboard tự động nhận diện và tích hợp
- Không cần sửa code chính

### ✅ **Tách biệt chức năng:**

- Mỗi module độc lập
- Dễ bảo trì và debug
- Có thể phát triển song song

### ✅ **Giao diện thống nhất:**

- Tất cả modules sử dụng cùng layout
- Navigation menu tự động
- Status bar và logging chung

### ✅ **Xuất .exe dễ dàng:**

- PyInstaller tự động đóng gói
- Tạo installer package
- Desktop shortcut tự động

## 🔮 Roadmap

### **v1.1.0 - Image Tools**

- Resize, crop, rotate images
- Convert formats (JPG, PNG, WebP)
- Batch processing

### **v1.2.0 - Text Tools**

- Text converter (case, encoding)
- Text analyzer (word count, readability)
- Text generator (lorem ipsum, passwords)

### **v1.3.0 - File Tools**

- File organizer
- Duplicate finder
- File converter

### **v1.4.0 - Network Tools**

- URL shortener
- Website checker
- Network scanner

## 🛠️ Development Setup

### **Cài đặt môi trường:**

```bash
# Tạo virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

# Cài đặt dependencies
pip install -r requirements.txt
```

### **Chạy development:**

```bash
python main_dashboard.py
```

### **Build production:**

```bash
python build_exe.py
```

## 📞 Hỗ trợ

- **Issues:** Tạo issue trên GitHub
- **Features:** Đề xuất tính năng mới
- **Bugs:** Báo cáo lỗi với thông tin chi tiết

## 📄 License

MIT License - Xem file LICENSE để biết thêm chi tiết.
