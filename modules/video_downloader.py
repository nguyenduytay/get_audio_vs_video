#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Downloader Module
Hỗ trợ tải video và audio từ Facebook, TikTok và các nền tảng khác
"""

import os
import re
import threading
import yt_dlp
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class VideoDownloaderModule:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        
        # Biến lưu trữ - phải khởi tạo trước setup_ui()
        self.download_path = tk.StringVar(value=str(Path.home() / "Downloads"))
        self.url_var = tk.StringVar()
        self.format_var = tk.StringVar(value="best")
        self.audio_only = tk.BooleanVar()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Thiết lập giao diện module"""
        # Main frame
        self.main_frame = ttk.Frame(self.parent_frame, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(self.main_frame, text="Video & Audio Downloader", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # URL input
        url_frame = ttk.Frame(self.main_frame)
        url_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(url_frame, text="URL Video:").pack(side=tk.LEFT)
        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=50)
        url_entry.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        
        # Format selection
        format_frame = ttk.Frame(self.main_frame)
        format_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(format_frame, text="Chất lượng:").pack(side=tk.LEFT)
        format_combo = ttk.Combobox(format_frame, textvariable=self.format_var, 
                                   values=["best", "worst", "bestvideo+bestaudio", "bestaudio", 
                                          "best[ext=mp4]", "best[height<=720]"])
        format_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        # Audio only checkbox
        audio_check = ttk.Checkbutton(format_frame, text="Chỉ tải audio", 
                                     variable=self.audio_only)
        audio_check.pack(side=tk.RIGHT)
        
        # Download path
        path_frame = ttk.Frame(self.main_frame)
        path_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(path_frame, text="Thư mục lưu:").pack(side=tk.LEFT)
        path_entry = ttk.Entry(path_frame, textvariable=self.download_path, width=40)
        path_entry.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        
        browse_btn = ttk.Button(path_frame, text="Chọn thư mục", command=self.browse_folder)
        browse_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        download_btn = ttk.Button(button_frame, text="Tải xuống", 
                                 command=self.start_download, style="Accent.TButton")
        download_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = ttk.Button(button_frame, text="Xóa", command=self.clear_fields)
        clear_btn.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=10)
        
        # Status label
        self.status_label = ttk.Label(self.main_frame, text="Sẵn sàng tải xuống")
        self.status_label.pack(pady=5)
        
        # Log text area
        log_frame = ttk.LabelFrame(self.main_frame, text="Nhật ký", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.log_text = tk.Text(log_frame, height=8, width=70)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def browse_folder(self):
        """Chọn thư mục lưu file"""
        folder = filedialog.askdirectory(initialdir=self.download_path.get())
        if folder:
            self.download_path.set(folder)
    
    def clear_fields(self):
        """Xóa các trường nhập liệu"""
        self.url_var.set("")
        self.log_text.delete(1.0, tk.END)
        self.status_label.config(text="Sẵn sàng tải xuống")
    
    def log_message(self, message):
        """Thêm thông báo vào log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.main_frame.update_idletasks()
    
    def validate_url(self, url):
        """Kiểm tra URL hợp lệ"""
        # Hỗ trợ nhiều nền tảng
        supported_patterns = [
            r'(?:https?://)?(?:www\.)?(?:facebook\.com|fb\.com|m\.facebook\.com)',
            r'(?:https?://)?(?:www\.)?(?:tiktok\.com|vm\.tiktok\.com|vt\.tiktok\.com)',
            r'(?:https?://)?(?:www\.)?(?:youtube\.com|youtu\.be)',
            r'(?:https?://)?(?:www\.)?(?:instagram\.com)',
            r'(?:https?://)?(?:www\.)?(?:twitter\.com|x\.com)',
            r'(?:https?://)?(?:www\.)?(?:vimeo\.com)',
            r'(?:https?://)?(?:www\.)?(?:dailymotion\.com)',
            r'(?:https?://)?(?:www\.)?(?:twitch\.tv)'
        ]
        
        return any(re.search(pattern, url) for pattern in supported_patterns)
    
    def check_video_availability(self, url):
        """Kiểm tra khả năng tải video"""
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                if info:
                    title = info.get('title', 'Unknown')
                    duration = info.get('duration', 0)
                    view_count = info.get('view_count', 0)
                    
                    self.log_message(f"✅ Video có thể tải: {title}")
                    self.log_message(f"📊 Thời lượng: {duration}s, Lượt xem: {view_count}")
                    return True
                else:
                    self.log_message("❌ Không thể lấy thông tin video")
                    return False
        except Exception as e:
            error_msg = str(e).lower()
            if 'private' in error_msg or 'unavailable' in error_msg:
                self.log_message("❌ Video riêng tư hoặc không khả dụng")
            elif 'copyright' in error_msg or 'blocked' in error_msg:
                self.log_message("❌ Video bị chặn do bản quyền")
            elif 'region' in error_msg or 'geo' in error_msg:
                self.log_message("❌ Video bị hạn chế theo vùng địa lý")
            else:
                self.log_message(f"❌ Lỗi: {str(e)}")
            return False
    
    def get_ydl_opts(self):
        """Cấu hình yt-dlp options"""
        format_selector = self.format_var.get()
        if self.audio_only.get():
            format_selector = "bestaudio"
        
        opts = {
            'outtmpl': os.path.join(self.download_path.get(), '%(title)s.%(ext)s'),
            'format': format_selector,
            'noplaylist': True,
            # Cấu hình cho TikTok
            'extractor_args': {
                'tiktok': {
                    'webpage_url_basename': 'video',
                    'api_hostname': 'api.tiktokv.com',
                }
            },
            # Thêm user agent để tránh bị chặn
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            },
            # Thử các format khác nhau nếu format yêu cầu không có
            'format_sort': ['res', 'ext:mp4:m4a'],
            'format_sort_force': True,
        }
        
        if self.audio_only.get():
            opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        
        return opts
    
    def progress_hook(self, d):
        """Hook để theo dõi tiến trình download"""
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                percent = d['downloaded_bytes'] / d['total_bytes'] * 100
                self.log_message(f"Đang tải: {percent:.1f}%")
            elif 'downloaded_bytes' in d:
                self.log_message(f"Đã tải: {d['downloaded_bytes']} bytes")
        elif d['status'] == 'finished':
            self.log_message(f"Hoàn thành: {d['filename']}")
    
    def download_video(self):
        """Tải video/audio"""
        url = self.url_var.get().strip()
        
        if not url:
            messagebox.showerror("Lỗi", "Vui lòng nhập URL!")
            return
        
        if not self.validate_url(url):
            messagebox.showerror("Lỗi", "URL không hợp lệ! Hỗ trợ: Facebook, TikTok, YouTube, Instagram, Twitter, Vimeo, Dailymotion, Twitch.")
            return
        
        try:
            self.progress.start()
            self.status_label.config(text="Đang kiểm tra video...")
            
            # Kiểm tra khả năng tải trước
            if not self.check_video_availability(url):
                self.status_label.config(text="Video không thể tải!")
                messagebox.showerror("Lỗi", "Video không thể tải! Có thể do:\n• Video riêng tư\n• Bị chặn bản quyền\n• Hạn chế theo vùng")
                return
            
            self.status_label.config(text="Đang tải xuống...")
            
            ydl_opts = self.get_ydl_opts()
            ydl_opts['progress_hooks'] = [self.progress_hook]
            
            # Thử tải với format linh hoạt hơn cho TikTok
            if 'tiktok.com' in url.lower():
                self.log_message("🔄 Đang tải video TikTok...")
                # Thử format khác nhau cho TikTok
                for format_try in [self.format_var.get(), "best", "worst", "best[ext=mp4]"]:
                    try:
                        ydl_opts['format'] = format_try
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([url])
                        break
                    except Exception as format_error:
                        self.log_message(f"⚠️ Thử format {format_try} thất bại: {str(format_error)}")
                        if format_try == "best[ext=mp4]":  # Lần thử cuối
                            raise format_error
            else:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
            self.log_message("✅ Tải xuống hoàn thành!")
            self.status_label.config(text="Tải xuống hoàn thành!")
            messagebox.showinfo("Thành công", "Tải xuống hoàn thành!")
            
        except Exception as e:
            error_msg = str(e).lower()
            if 'private' in error_msg or 'unavailable' in error_msg:
                self.log_message("❌ Video riêng tư hoặc không khả dụng")
                messagebox.showerror("Lỗi", "Video riêng tư hoặc không khả dụng!")
            elif 'copyright' in error_msg or 'blocked' in error_msg:
                self.log_message("❌ Video bị chặn do bản quyền")
                messagebox.showerror("Lỗi", "Video bị chặn do bản quyền!\n\n⚠️ Không thể tải video có bản quyền nghiêm ngặt.\nHãy tìm nội dung công khai hoặc xin phép sử dụng.")
            elif 'region' in error_msg or 'geo' in error_msg:
                self.log_message("❌ Video bị hạn chế theo vùng địa lý")
                messagebox.showerror("Lỗi", "Video bị hạn chế theo vùng địa lý!\n\n⚠️ Video chỉ dành cho một số quốc gia.\nHãy tìm nội dung không bị hạn chế theo vùng.")
            elif 'format' in error_msg and 'not available' in error_msg:
                self.log_message("❌ Format không khả dụng")
                messagebox.showerror("Lỗi", "Format video không khả dụng!\n\n💡 Thử chọn format khác:\n• best\n• worst\n• best[ext=mp4]")
            else:
                self.log_message(f"❌ Lỗi: {str(e)}")
                messagebox.showerror("Lỗi", f"Lỗi: {str(e)}")
            
            self.status_label.config(text="Có lỗi xảy ra!")
        
        finally:
            self.progress.stop()
    
    def start_download(self):
        """Bắt đầu tải xuống trong thread riêng"""
        thread = threading.Thread(target=self.download_video)
        thread.daemon = True
        thread.start()
