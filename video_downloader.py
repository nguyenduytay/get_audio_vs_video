#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Facebook và TikTok Video/Audio Downloader
Hỗ trợ tải video và audio từ Facebook và TikTok
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import yt_dlp
from pathlib import Path
import re

class VideoDownloader:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Facebook & TikTok Downloader")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Biến lưu trữ
        self.download_path = tk.StringVar(value=str(Path.home() / "Downloads"))
        self.url_var = tk.StringVar()
        self.format_var = tk.StringVar(value="best")
        self.audio_only = tk.BooleanVar()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Thiết lập giao diện người dùng"""
        # Frame chính
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Cấu hình grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="Facebook & TikTok Downloader", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Cảnh báo pháp lý
        warning_label = ttk.Label(main_frame, 
                                 text="⚠️ Chỉ tải nội dung công khai và có quyền sử dụng", 
                                 font=("Arial", 9), foreground="red")
        warning_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # URL input
        ttk.Label(main_frame, text="URL Video:").grid(row=1, column=0, sticky=tk.W, pady=5)
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=50)
        url_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # Format selection
        ttk.Label(main_frame, text="Chất lượng:").grid(row=2, column=0, sticky=tk.W, pady=5)
        format_combo = ttk.Combobox(main_frame, textvariable=self.format_var, 
                                   values=["best", "worst", "bestvideo+bestaudio", "bestaudio"])
        format_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # Audio only checkbox
        audio_check = ttk.Checkbutton(main_frame, text="Chỉ tải audio", 
                                     variable=self.audio_only)
        audio_check.grid(row=2, column=2, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Download path
        ttk.Label(main_frame, text="Thư mục lưu:").grid(row=3, column=0, sticky=tk.W, pady=5)
        path_entry = ttk.Entry(main_frame, textvariable=self.download_path, width=40)
        path_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        browse_btn = ttk.Button(main_frame, text="Chọn thư mục", command=self.browse_folder)
        browse_btn.grid(row=3, column=2, pady=5, padx=(5, 0))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        download_btn = ttk.Button(button_frame, text="Tải xuống", 
                                 command=self.start_download, style="Accent.TButton")
        download_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = ttk.Button(button_frame, text="Xóa", command=self.clear_fields)
        clear_btn.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Sẵn sàng tải xuống")
        self.status_label.grid(row=6, column=0, columnspan=3, pady=5)
        
        # Log text area
        log_frame = ttk.LabelFrame(main_frame, text="Nhật ký", padding="5")
        log_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(log_frame, height=8, width=70)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Cấu hình grid weights
        main_frame.rowconfigure(7, weight=1)
        
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
        self.root.update_idletasks()
    
    def validate_url(self, url):
        """Kiểm tra URL hợp lệ"""
        facebook_pattern = r'(?:https?://)?(?:www\.)?(?:facebook\.com|fb\.com|m\.facebook\.com)'
        tiktok_pattern = r'(?:https?://)?(?:www\.)?(?:tiktok\.com|vm\.tiktok\.com|vt\.tiktok\.com)'
        
        return bool(re.search(facebook_pattern, url) or re.search(tiktok_pattern, url))
    
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
            messagebox.showerror("Lỗi", "URL không hợp lệ! Chỉ hỗ trợ Facebook và TikTok.")
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
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Tải xuống
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
    
    def run(self):
        """Chạy ứng dụng"""
        self.root.mainloop()

def main():
    """Hàm main"""
    try:
        app = VideoDownloader()
        app.run()
    except Exception as e:
        print(f"Lỗi khởi động ứng dụng: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
