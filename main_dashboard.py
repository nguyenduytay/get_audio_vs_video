#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Dashboard - Multi-Utility Application
Dashboard đa chức năng với khả năng mở rộng
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from pathlib import Path

# Import modules
from modules.video_downloader import VideoDownloaderModule

class MainDashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Multi-Utility Dashboard")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Biến lưu trữ
        self.current_module = None
        self.modules = {}
        
        self.setup_ui()
        self.load_modules()
        
    def setup_ui(self):
        """Thiết lập giao diện dashboard"""
        # Cấu hình grid
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Sidebar
        self.setup_sidebar()
        
        # Main content area
        self.setup_main_content()
        
        # Status bar
        self.setup_status_bar()
        
    def setup_sidebar(self):
        """Thiết lập sidebar menu"""
        self.sidebar = ttk.Frame(self.root, width=200, padding="10")
        self.sidebar.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W))
        self.sidebar.grid_propagate(False)
        
        # Logo/Title
        title_label = ttk.Label(self.sidebar, text="Multi-Utility\nDashboard", 
                               font=("Arial", 14, "bold"), justify=tk.CENTER)
        title_label.pack(pady=(0, 20))
        
        # Menu buttons
        self.menu_buttons = {}
        
        # Video Downloader
        self.menu_buttons['video_downloader'] = ttk.Button(
            self.sidebar, text="📥 Video Downloader", 
            command=lambda: self.switch_module('video_downloader'),
            width=20
        )
        self.menu_buttons['video_downloader'].pack(pady=5, fill=tk.X)
        
        # Placeholder for future modules
        self.menu_buttons['image_tools'] = ttk.Button(
            self.sidebar, text="🖼️ Image Tools", 
            command=lambda: self.switch_module('image_tools'),
            width=20, state=tk.DISABLED
        )
        self.menu_buttons['image_tools'].pack(pady=5, fill=tk.X)
        
        self.menu_buttons['text_tools'] = ttk.Button(
            self.sidebar, text="📝 Text Tools", 
            command=lambda: self.switch_module('text_tools'),
            width=20, state=tk.DISABLED
        )
        self.menu_buttons['text_tools'].pack(pady=5, fill=tk.X)
        
        self.menu_buttons['file_tools'] = ttk.Button(
            self.sidebar, text="📁 File Tools", 
            command=lambda: self.switch_module('file_tools'),
            width=20, state=tk.DISABLED
        )
        self.menu_buttons['file_tools'].pack(pady=5, fill=tk.X)
        
        # Separator
        ttk.Separator(self.sidebar, orient='horizontal').pack(fill=tk.X, pady=20)
        
        # Settings
        settings_btn = ttk.Button(
            self.sidebar, text="⚙️ Settings", 
            command=self.open_settings, width=20
        )
        settings_btn.pack(pady=5, fill=tk.X)
        
        # About
        about_btn = ttk.Button(
            self.sidebar, text="ℹ️ About", 
            command=self.show_about, width=20
        )
        about_btn.pack(pady=5, fill=tk.X)
        
        # Exit
        exit_btn = ttk.Button(
            self.sidebar, text="❌ Exit", 
            command=self.root.quit, width=20
        )
        exit_btn.pack(pady=5, fill=tk.X)
        
    def setup_main_content(self):
        """Thiết lập vùng nội dung chính"""
        self.main_content = ttk.Frame(self.root, padding="10")
        self.main_content.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        # Welcome screen
        self.show_welcome()
        
    def setup_status_bar(self):
        """Thiết lập thanh trạng thái"""
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(self.status_frame, text="Sẵn sàng")
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Version info
        version_label = ttk.Label(self.status_frame, text="v1.0.0")
        version_label.pack(side=tk.RIGHT, padx=10, pady=5)
        
    def load_modules(self):
        """Tải các modules"""
        try:
            # Video Downloader Module
            self.modules['video_downloader'] = VideoDownloaderModule
            self.status_label.config(text="Modules loaded successfully")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải modules: {e}")
            self.status_label.config(text="Error loading modules")
    
    def switch_module(self, module_name):
        """Chuyển đổi module"""
        try:
            # Clear current content
            for widget in self.main_content.winfo_children():
                widget.destroy()
            
            # Update button states
            for name, button in self.menu_buttons.items():
                if name == module_name:
                    button.state(['pressed'])
                else:
                    button.state(['!pressed'])
            
            # Load new module
            if module_name in self.modules:
                if module_name == 'video_downloader':
                    self.current_module = self.modules[module_name](self.main_content)
                    self.status_label.config(text="Video Downloader - Sẵn sàng tải video/audio")
                    print(f"✅ Module {module_name} loaded successfully")
                else:
                    self.show_coming_soon(module_name)
            else:
                self.show_coming_soon(module_name)
                
        except Exception as e:
            print(f"❌ Error switching module: {e}")
            messagebox.showerror("Lỗi", f"Không thể chuyển đổi module: {e}")
    
    def show_welcome(self):
        """Hiển thị màn hình chào mừng"""
        welcome_frame = ttk.Frame(self.main_content)
        welcome_frame.pack(expand=True, fill=tk.BOTH)
        
        # Welcome message
        welcome_label = ttk.Label(welcome_frame, 
                                 text="Chào mừng đến với Multi-Utility Dashboard", 
                                 font=("Arial", 20, "bold"))
        welcome_label.pack(pady=50)
        
        # Description
        desc_label = ttk.Label(welcome_frame, 
                              text="Dashboard đa chức năng với khả năng mở rộng\nChọn một tiện ích từ menu bên trái để bắt đầu", 
                              font=("Arial", 12), justify=tk.CENTER)
        desc_label.pack(pady=20)
        
        # Features
        features_frame = ttk.LabelFrame(welcome_frame, text="Tính năng hiện có", padding="20")
        features_frame.pack(pady=30, fill=tk.X)
        
        features = [
            "📥 Video Downloader - Tải video/audio từ nhiều nền tảng",
            "🖼️ Image Tools - Công cụ xử lý hình ảnh (sắp ra mắt)",
            "📝 Text Tools - Công cụ xử lý văn bản (sắp ra mắt)",
            "📁 File Tools - Công cụ quản lý file (sắp ra mắt)"
        ]
        
        for feature in features:
            ttk.Label(features_frame, text=feature, font=("Arial", 10)).pack(anchor=tk.W, pady=5)
        
        # Quick start
        quick_start_frame = ttk.LabelFrame(welcome_frame, text="Bắt đầu nhanh", padding="20")
        quick_start_frame.pack(pady=20, fill=tk.X)
        
        start_btn = ttk.Button(quick_start_frame, text="🚀 Bắt đầu với Video Downloader", 
                              command=lambda: self.switch_module('video_downloader'),
                              style="Accent.TButton")
        start_btn.pack()
    
    def show_coming_soon(self, module_name):
        """Hiển thị thông báo sắp ra mắt"""
        coming_soon_frame = ttk.Frame(self.main_content)
        coming_soon_frame.pack(expand=True, fill=tk.BOTH)
        
        # Coming soon message
        coming_soon_label = ttk.Label(coming_soon_frame, 
                                     text="🚧 Tính năng đang phát triển", 
                                     font=("Arial", 18, "bold"))
        coming_soon_label.pack(pady=50)
        
        module_names = {
            'image_tools': 'Image Tools',
            'text_tools': 'Text Tools', 
            'file_tools': 'File Tools'
        }
        
        module_display_name = module_names.get(module_name, module_name)
        
        desc_label = ttk.Label(coming_soon_frame, 
                              text=f"{module_display_name} sẽ sớm ra mắt!\n\nChúng tôi đang phát triển tính năng này.\nHãy quay lại sau.", 
                              font=("Arial", 12), justify=tk.CENTER)
        desc_label.pack(pady=20)
        
        # Back button
        back_btn = ttk.Button(coming_soon_frame, text="← Quay lại", 
                             command=self.show_welcome)
        back_btn.pack(pady=20)
    
    def open_settings(self):
        """Mở cài đặt"""
        messagebox.showinfo("Settings", "Tính năng cài đặt sẽ sớm ra mắt!")
    
    def show_about(self):
        """Hiển thị thông tin về ứng dụng"""
        about_text = """Multi-Utility Dashboard v1.0.0

Dashboard đa chức năng với khả năng mở rộng

Tính năng hiện có:
• Video Downloader - Tải video/audio từ nhiều nền tảng

Tính năng sắp ra mắt:
• Image Tools - Công cụ xử lý hình ảnh
• Text Tools - Công cụ xử lý văn bản  
• File Tools - Công cụ quản lý file

Phát triển bởi: Your Name
Liên hệ: your.email@example.com"""
        
        messagebox.showinfo("About", about_text)
    
    def run(self):
        """Chạy ứng dụng"""
        self.root.mainloop()

def main():
    """Hàm main"""
    try:
        app = MainDashboard()
        app.run()
    except Exception as e:
        print(f"Lỗi khởi động ứng dụng: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
