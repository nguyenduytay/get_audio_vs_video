#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Assistant Module
Tích hợp Google Gemini AI để hỗ trợ người dùng
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from pathlib import Path
import webbrowser

# Try to import AI libraries
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

# Kiểm tra provider nào thực sự hoạt động
AVAILABLE_PROVIDERS = []
if GEMINI_AVAILABLE:
    AVAILABLE_PROVIDERS.append("google")
# OpenAI không tương thích với Google Gemini API
# Anthropic không tương thích với Google Gemini API

class AIAssistantModule:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        
        # Biến lưu trữ
        self.api_key = tk.StringVar()
        self.user_input = tk.StringVar()
        self.ai_provider = tk.StringVar(value="google")
        self.model_name = tk.StringVar(value="gemini-2.0-flash-exp")
        
        # AI clients
        self.gemini_client = None
        self.openai_client = None
        self.anthropic_client = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Thiết lập giao diện module"""
        # Main frame
        self.main_frame = ttk.Frame(self.parent_frame, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(self.main_frame, text="AI Assistant (Google Gemini)", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # API Key setup
        api_frame = ttk.LabelFrame(self.main_frame, text="Cấu hình API", padding="10")
        api_frame.pack(fill=tk.X, pady=(0, 10))
        
        # API Key input
        key_frame = ttk.Frame(api_frame)
        key_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(key_frame, text="API Key:").pack(side=tk.LEFT)
        api_entry = ttk.Entry(key_frame, textvariable=self.api_key, width=50, show="*")
        api_entry.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        
        save_key_btn = ttk.Button(key_frame, text="Lưu", command=self.save_api_key)
        save_key_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # AI Provider selection
        provider_frame = ttk.Frame(api_frame)
        provider_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(provider_frame, text="AI Provider:").pack(side=tk.LEFT)
        provider_combo = ttk.Combobox(provider_frame, textvariable=self.ai_provider, 
                                     values=AVAILABLE_PROVIDERS)
        provider_combo.pack(side=tk.LEFT, padx=(10, 0))
        provider_combo.bind('<<ComboboxSelected>>', self.on_provider_change)
        
        # Nếu không có provider nào, thêm Google làm mặc định
        if not AVAILABLE_PROVIDERS:
            AVAILABLE_PROVIDERS.append("google")
            self.ai_provider.set("google")
        
        # Model selection
        model_frame = ttk.Frame(api_frame)
        model_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(model_frame, text="Model:").pack(side=tk.LEFT)
        self.model_combo = ttk.Combobox(model_frame, textvariable=self.model_name)
        self.model_combo.pack(side=tk.LEFT, padx=(10, 0))
        self.update_model_list()
        
        # Status
        self.status_label = ttk.Label(api_frame, text="Chưa kết nối")
        self.status_label.pack(pady=5)
        
        # Chat interface
        chat_frame = ttk.LabelFrame(self.main_frame, text="Trò chuyện với AI", padding="10")
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Chat history
        self.chat_text = scrolledtext.ScrolledText(chat_frame, height=15, width=70, 
                                                   state=tk.DISABLED, wrap=tk.WORD)
        self.chat_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Input area
        input_frame = ttk.Frame(chat_frame)
        input_frame.pack(fill=tk.X)
        
        ttk.Label(input_frame, text="Câu hỏi:").pack(side=tk.LEFT)
        input_entry = ttk.Entry(input_frame, textvariable=self.user_input, width=50)
        input_entry.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        input_entry.bind('<Return>', lambda e: self.send_message())
        
        send_btn = ttk.Button(input_frame, text="Gửi", command=self.send_message)
        send_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        clear_btn = ttk.Button(button_frame, text="Xóa cuộc trò chuyện", 
                              command=self.clear_chat)
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        test_btn = ttk.Button(button_frame, text="Test kết nối", 
                             command=self.test_connection)
        test_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        model_info_btn = ttk.Button(button_frame, text="ℹ️ Thông tin Model", 
                                   command=self.show_model_info)
        model_info_btn.pack(side=tk.LEFT)
        
        # Load saved API key
        self.load_api_key()
        
        # Check Gemini availability
        if not GEMINI_AVAILABLE:
            self.add_to_chat("❌ Google Gemini không được cài đặt!\n"
                           "Chạy: pip install google-generativeai")
            self.status_label.config(text="Gemini không khả dụng")
        else:
            # Hiển thị hướng dẫn sử dụng
            self.add_to_chat("🤖 Chào mừng đến với AI Assistant!")
            self.add_to_chat(f"✅ Provider khả dụng: {', '.join(AVAILABLE_PROVIDERS).upper()}")
            self.add_to_chat("📝 Để sử dụng:")
            self.add_to_chat("  1. Lấy API Key (click button bên dưới)")
            self.add_to_chat("  2. Nhập API Key vào ô bên trên")
            self.add_to_chat("  3. Click 'Lưu' để lưu API Key")
            self.add_to_chat("  4. Click 'Test kết nối' để kiểm tra")
            self.add_to_chat("  5. Bắt đầu trò chuyện với AI!")
            self.add_to_chat("")
            self.add_to_chat("💡 Bạn có thể hỏi AI về bất kỳ chủ đề nào!")
            
            # Thêm button mở Google AI Studio
            self.add_get_api_button()
    
    def load_api_key(self):
        """Tải API key đã lưu"""
        try:
            key_file = Path("ai_api_key.txt")
            if key_file.exists():
                with open(key_file, 'r') as f:
                    self.api_key.set(f.read().strip())
                self.connect_to_gemini()
        except Exception as e:
            print(f"Error loading API key: {e}")
    
    def save_api_key(self):
        """Lưu API key"""
        try:
            key_file = Path("ai_api_key.txt")
            with open(key_file, 'w') as f:
                f.write(self.api_key.get())
            self.connect_to_gemini()
            messagebox.showinfo("Thành công", "API Key đã được lưu!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu API Key: {e}")
    
    def connect_to_gemini(self):
        """Kết nối với Google Gemini"""
        if not GEMINI_AVAILABLE:
            self.status_label.config(text="Gemini không khả dụng")
            return False
        
        api_key = self.api_key.get().strip()
        if not api_key:
            self.status_label.config(text="Chưa nhập API Key")
            return False
        
        try:
            # Configure API key
            genai.configure(api_key=api_key)
            self.client = genai
            self.status_label.config(text="Đã kết nối")
            self.add_to_chat("✅ Đã kết nối với Google Gemini!")
            return True
        except Exception as e:
            self.status_label.config(text="Kết nối thất bại")
            self.add_to_chat(f"❌ Lỗi kết nối: {str(e)}")
            return False
    
    def test_connection(self):
        """Test kết nối với Gemini"""
        if not self.connect_to_gemini():
            return
        
        try:
            self.add_to_chat("🔄 Đang test kết nối...")
            model = self.client.GenerativeModel(self.model_name.get())
            response = model.generate_content("Xin chào! Bạn có thể trả lời bằng tiếng Việt không?")
            self.add_to_chat(f"🤖 AI: {response.text}")
        except Exception as e:
            self.add_to_chat(f"❌ Test thất bại: {str(e)}")
    
    def send_message(self):
        """Gửi tin nhắn đến AI"""
        user_message = self.user_input.get().strip()
        if not user_message:
            return
        
        # Thêm tin nhắn người dùng vào chat
        self.add_to_chat(f"👤 Bạn: {user_message}")
        self.user_input.set("")
        
        # Kiểm tra API key
        api_key = self.api_key.get().strip()
        if not api_key:
            # Chế độ demo - AI giả lập thông minh
            self.add_to_chat("🤖 AI (Demo): " + self.get_demo_response(user_message))
            return
        
        # Kết nối nếu chưa có
        if not self.client:
            if not self.connect_to_gemini():
                return
        
        # Gửi đến AI trong thread riêng
        thread = threading.Thread(target=self.get_ai_response, args=(user_message,))
        thread.daemon = True
        thread.start()
    
    def get_ai_response(self, message):
        """Lấy phản hồi từ AI"""
        try:
            self.add_to_chat("🤖 AI đang suy nghĩ...")
            
            model = self.client.GenerativeModel(self.model_name.get())
            response = model.generate_content(message)
            
            # Xóa dòng "AI đang suy nghĩ..."
            self.chat_text.config(state=tk.NORMAL)
            self.chat_text.delete("end-2l", "end-1l")
            self.chat_text.config(state=tk.DISABLED)
            
            self.add_to_chat(f"🤖 AI: {response.text}")
            
        except Exception as e:
            self.add_to_chat(f"❌ Lỗi: {str(e)}")
    
    def add_to_chat(self, message):
        """Thêm tin nhắn vào chat"""
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, f"{message}\n\n")
        self.chat_text.see(tk.END)
        self.chat_text.config(state=tk.DISABLED)
        self.main_frame.update_idletasks()
    
    def add_get_api_button(self):
        """Thêm button để mở Google AI Studio"""
        # Tạo frame cho button
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Button mở Google AI Studio
        get_api_btn = ttk.Button(button_frame, text="🔑 Lấy API Key từ Google AI Studio", 
                                command=self.open_google_ai_studio, width=40)
        get_api_btn.pack(pady=5)
        
        # Button hướng dẫn
        help_btn = ttk.Button(button_frame, text="❓ Hướng dẫn sử dụng API Key", 
                             command=self.show_api_help, width=40)
        help_btn.pack(pady=5)
    
    def open_google_ai_studio(self):
        """Mở Google AI Studio trong browser"""
        try:
            webbrowser.open("https://makersuite.google.com/app/apikey")
            self.add_to_chat("🌐 Đã mở Google AI Studio trong browser!")
            self.add_to_chat("📝 Hướng dẫn:")
            self.add_to_chat("  1. Đăng nhập bằng tài khoản Google")
            self.add_to_chat("  2. Click 'Create API Key' hoặc 'Tạo API Key'")
            self.add_to_chat("  3. Copy API key được tạo")
            self.add_to_chat("  4. Paste vào ô 'API Key' bên trên")
            self.add_to_chat("  5. Click 'Lưu' để lưu API Key")
        except Exception as e:
            self.add_to_chat(f"❌ Không thể mở browser: {e}")
            self.add_to_chat("💡 Vui lòng truy cập thủ công: https://makersuite.google.com/app/apikey")
    
    def update_model_list(self):
        """Cập nhật danh sách model theo provider"""
        provider = self.ai_provider.get()
        
        if provider == "google" and GEMINI_AVAILABLE:
            models = ["gemini-2.0-flash-exp", "gemini-1.5-pro", "gemini-1.5-flash", 
                     "gemini-1.5-pro-latest", "gemini-1.5-flash-latest"]
            self.model_name.set("gemini-2.0-flash-exp")
        # OpenAI không tương thích với Google Gemini API
        # Anthropic không tương thích với Google Gemini API
        else:
            # Fallback về Google nếu provider không khả dụng
            models = ["gemini-2.0-flash-exp"]
            self.model_name.set("gemini-2.0-flash-exp")
            self.ai_provider.set("google")
        
        self.model_combo['values'] = models
    
    def on_provider_change(self, event=None):
        """Xử lý khi thay đổi AI provider"""
        self.update_model_list()
        self.add_to_chat(f"🔄 Đã chuyển sang {self.ai_provider.get().upper()} AI")
        self.show_provider_info()
    
    def show_provider_info(self):
        """Hiển thị thông tin về AI provider hiện tại"""
        provider = self.ai_provider.get()
        
        if provider == "google" and GEMINI_AVAILABLE:
            self.add_to_chat("🔍 Google Gemini AI:")
            self.add_to_chat("  - Miễn phí với giới hạn")
            self.add_to_chat("  - Hỗ trợ đa ngôn ngữ tốt")
            self.add_to_chat("  - Tốc độ nhanh, chất lượng cao")
        # OpenAI không tương thích với Google Gemini API
        # Anthropic không tương thích với Google Gemini API
        else:
            self.add_to_chat("❌ Provider không khả dụng!")
            self.add_to_chat("💡 Chuyển về Google Gemini (mặc định)")
            self.ai_provider.set("google")
            self.update_model_list()
    
    def show_model_info(self):
        """Hiển thị thông tin về các model AI"""
        provider = self.ai_provider.get()
        
        if provider == "google" and GEMINI_AVAILABLE:
            self.add_to_chat("🤖 Google Gemini Models:")
            self.add_to_chat("🚀 gemini-2.0-flash-exp - Mới nhất, mạnh nhất")
            self.add_to_chat("🧠 gemini-1.5-pro - Chuyên sâu, suy luận phức tạp")
            self.add_to_chat("⚡ gemini-1.5-flash - Nhanh, chat thường ngày")
        # OpenAI không tương thích với Google Gemini API
        # Anthropic không tương thích với Google Gemini API
        else:
            self.add_to_chat("❌ Provider không khả dụng!")
            self.add_to_chat("💡 Chuyển về Google Gemini (mặc định)")
            self.ai_provider.set("google")
            self.update_model_list()
    
    def show_api_help(self):
        """Hiển thị hướng dẫn chi tiết về API Key"""
        self.add_to_chat("📚 Hướng dẫn chi tiết về API Key:")
        self.add_to_chat("")
        self.add_to_chat("🔑 API Key là gì?")
        self.add_to_chat("  - Mã xác thực để sử dụng Google Gemini AI")
        self.add_to_chat("  - Miễn phí nhưng có giới hạn sử dụng")
        self.add_to_chat("  - Cần tài khoản Google để tạo")
        self.add_to_chat("")
        self.add_to_chat("📝 Cách lấy API Key:")
        self.add_to_chat("  1. Truy cập: https://makersuite.google.com/app/apikey")
        self.add_to_chat("  2. Đăng nhập bằng tài khoản Google")
        self.add_to_chat("  3. Click 'Create API Key'")
        self.add_to_chat("  4. Chọn project hoặc tạo project mới")
        self.add_to_chat("  5. Copy API key được tạo")
        self.add_to_chat("")
        self.add_to_chat("⚠️ Lưu ý bảo mật:")
        self.add_to_chat("  - Không chia sẻ API key với người khác")
        self.add_to_chat("  - API key sẽ được lưu tự động trong file ai_api_key.txt")
        self.add_to_chat("  - Có thể xóa và tạo lại API key mới bất kỳ lúc nào")
    
    def clear_chat(self):
        """Xóa cuộc trò chuyện"""
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.delete(1.0, tk.END)
        self.chat_text.config(state=tk.DISABLED)
        self.add_to_chat("💬 Cuộc trò chuyện đã được xóa.")
