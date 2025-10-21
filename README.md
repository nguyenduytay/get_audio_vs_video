# Facebook & TikTok Video/Audio Downloader

Ứng dụng Python để tải video và audio từ Facebook và TikTok với giao diện đồ họa đơn giản.

## Tính năng

- ✅ Tải video từ Facebook và TikTok
- ✅ Tải audio từ video (chuyển đổi sang MP3)
- ✅ Chọn chất lượng video/audio
- ✅ Giao diện đồ họa thân thiện
- ✅ Theo dõi tiến trình tải xuống
- ✅ Chọn thư mục lưu file

## Yêu cầu hệ thống

- Python 3.7 trở lên
- FFmpeg (để chuyển đổi audio)

## Cài đặt

### 🚀 Cài đặt nhanh (Khuyến nghị)

**Windows:**

```bash
# Chạy file setup tự động
setup_venv.bat
```

**Linux/macOS:**

```bash
# Tạo môi trường ảo thủ công
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 📋 Cài đặt thủ công

### 1. Clone repository

```bash
git clone <repository-url>
cd get_video_vs_audio
```

### 2. Tạo môi trường ảo (Virtual Environment)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Cài đặt dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Cài đặt FFmpeg

**Windows:**

1. Tải FFmpeg từ https://ffmpeg.org/download.html
2. Giải nén và thêm vào PATH

**macOS:**

```bash
brew install ffmpeg
```

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install ffmpeg
```

## Sử dụng

### Chạy ứng dụng

**Cách 1: Sử dụng script tự động (Windows)**

```bash
run.bat
```

**Cách 2: Chạy thủ công**

```bash
# Windows
venv\Scripts\activate
python video_downloader.py

# Linux/macOS
source venv/bin/activate
python video_downloader.py
```

### Cách sử dụng

1. Mở ứng dụng
2. Nhập URL video Facebook hoặc TikTok
3. Chọn chất lượng (best, worst, bestvideo+bestaudio, bestaudio)
4. Chọn thư mục lưu file
5. Nhấn "Tải xuống"

### Ví dụ URL hỗ trợ

- Facebook: `https://www.facebook.com/watch/?v=123456789`
- TikTok: `https://www.tiktok.com/@username/video/123456789`

## Cấu trúc dự án

```
get_video_vs_audio/
├── video_downloader.py    # Script chính
├── requirements.txt       # Dependencies
├── setup_venv.bat         # Setup tự động (Windows)
├── run.bat                # Chạy ứng dụng (Windows)
├── venv/                 # Môi trường ảo (tự tạo)
└── README.md             # Hướng dẫn
```

## Lưu ý quan trọng

⚠️ **Tuân thủ điều khoản sử dụng:**

- Chỉ tải nội dung mà bạn có quyền truy cập
- Tôn trọng bản quyền và quyền riêng tư
- Sử dụng cho mục đích cá nhân, không thương mại

## Xử lý lỗi thường gặp

### Lỗi "FFmpeg not found"

- Đảm bảo FFmpeg đã được cài đặt và có trong PATH

### Lỗi "Video unavailable"

- Kiểm tra URL có đúng không
- Video có thể bị hạn chế quyền truy cập

### Lỗi "Network error"

- Kiểm tra kết nối internet
- Thử lại sau vài phút

## Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng tạo issue hoặc pull request.

## License

MIT License - Xem file LICENSE để biết thêm chi tiết.
