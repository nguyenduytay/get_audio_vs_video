#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Image Tools Module
Hỗ trợ chuyển đổi SVG sang PNG với tùy chỉnh kích thước và margin
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import cairosvg
from pathlib import Path
import threading
import xml.etree.ElementTree as ET
import re

class ImageToolsModule:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        
        # Biến lưu trữ
        self.svg_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.width = tk.StringVar(value="1024")
        self.height = tk.StringVar(value="1024")
        self.margin_percent = tk.StringVar(value="20")
        self.bg_color = tk.StringVar(value="") # Empty for transparent
        
        self.setup_ui()
        
    def setup_ui(self):
        """Thiết lập giao diện module"""
        # Main frame
        self.main_frame = ttk.Frame(self.parent_frame, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(self.main_frame, text="Advanced SVG to PNG Tool", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 10))

        # Notebook for Single/Batch modes
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Single conversion tab
        self.single_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.single_frame, text="Đơn lẻ")
        self.setup_single_ui()
        
        # Batch conversion tab
        self.batch_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.batch_frame, text="Hàng loạt")
        self.setup_batch_ui()
        
        # Shared Settings
        self.setup_shared_settings()
        
        # Progress & Status (Shared)
        self.progress = ttk.Progressbar(self.main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=10)
        
        self.status_label = ttk.Label(self.main_frame, text="Sẵn sàng")
        self.status_label.pack(pady=5)

    def setup_single_ui(self):
        # Input SVG
        input_frame = ttk.Frame(self.single_frame)
        input_frame.pack(fill=tk.X, pady=5)
        ttk.Label(input_frame, text="SVG Input:", width=12).pack(side=tk.LEFT)
        ttk.Entry(input_frame, textvariable=self.svg_path).pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        ttk.Button(input_frame, text="Chọn File", command=self.browse_svg).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Output PNG
        output_frame = ttk.Frame(self.single_frame)
        output_frame.pack(fill=tk.X, pady=5)
        ttk.Label(output_frame, text="PNG Output:", width=12).pack(side=tk.LEFT)
        ttk.Entry(output_frame, textvariable=self.output_path).pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        ttk.Button(output_frame, text="Lưu tại...", command=self.browse_output).pack(side=tk.RIGHT, padx=(5, 0))
        
        ttk.Button(self.single_frame, text="Chuyển đổi ngay", 
                   command=self.start_single_conversion, style="Accent.TButton").pack(pady=10)

    def setup_batch_ui(self):
        self.batch_input_dir = tk.StringVar()
        self.batch_output_dir = tk.StringVar()
        
        # Input Dir
        in_frame = ttk.Frame(self.batch_frame)
        in_frame.pack(fill=tk.X, pady=5)
        ttk.Label(in_frame, text="Thư mục SVG:", width=12).pack(side=tk.LEFT)
        ttk.Entry(in_frame, textvariable=self.batch_input_dir).pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        ttk.Button(in_frame, text="Chọn", command=lambda: self.browse_dir(self.batch_input_dir)).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Output Dir
        out_frame = ttk.Frame(self.batch_frame)
        out_frame.pack(fill=tk.X, pady=5)
        ttk.Label(out_frame, text="Thư mục PNG:", width=12).pack(side=tk.LEFT)
        ttk.Entry(out_frame, textvariable=self.batch_output_dir).pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        ttk.Button(out_frame, text="Chọn", command=lambda: self.browse_dir(self.batch_output_dir)).pack(side=tk.RIGHT, padx=(5, 0))
        
        ttk.Button(self.batch_frame, text="Bắt đầu Batch", 
                   command=self.start_batch_conversion, style="Accent.TButton").pack(pady=10)

    def setup_shared_settings(self):
        settings_frame = ttk.LabelFrame(self.main_frame, text="Cấu hình chung", padding="10")
        settings_frame.pack(fill=tk.X, pady=10)
        
        size_frame = ttk.Frame(settings_frame)
        size_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(size_frame, text="Kích thước (px):").pack(side=tk.LEFT)
        ttk.Entry(size_frame, textvariable=self.width, width=8).pack(side=tk.LEFT, padx=(5, 5))
        ttk.Label(size_frame, text="x").pack(side=tk.LEFT)
        ttk.Entry(size_frame, textvariable=self.height, width=8).pack(side=tk.LEFT, padx=(5, 15))
        
        ttk.Label(size_frame, text="Margin (%):").pack(side=tk.LEFT)
        ttk.Entry(size_frame, textvariable=self.margin_percent, width=8).pack(side=tk.LEFT, padx=(5, 0))
        
        color_frame = ttk.Frame(settings_frame)
        color_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(color_frame, text="Màu nền:").pack(side=tk.LEFT)
        ttk.Entry(color_frame, textvariable=self.bg_color, width=15).pack(side=tk.LEFT, padx=(5, 5))
        ttk.Button(color_frame, text="Chọn màu", command=self.choose_color).pack(side=tk.LEFT)
        ttk.Label(color_frame, text="(Để trống = trong suốt)", font=("Arial", 8, "italic")).pack(side=tk.LEFT, padx=10)

    def choose_color(self):
        color = colorchooser.askcolor(title="Chọn màu nền")
        if color[1]:
            self.bg_color.set(color[1])

    def browse_svg(self):
        file_path = filedialog.askopenfilename(filetypes=[("SVG files", "*.svg")])
        if file_path:
            self.svg_path.set(file_path)
            if not self.output_path.get():
                self.output_path.set(str(Path(file_path).with_suffix('.png')))

    def browse_output(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path: self.output_path.set(file_path)

    def browse_dir(self, var):
        folder = filedialog.askdirectory()
        if folder: var.set(folder)

    def start_single_conversion(self):
        if not self.svg_path.get():
            messagebox.showerror("Lỗi", "Hãy chọn file SVG!")
            return
        thread = threading.Thread(target=self.convert_single_process)
        thread.daemon = True
        thread.start()

    def start_batch_conversion(self):
        if not self.batch_input_dir.get():
            messagebox.showerror("Lỗi", "Hãy chọn thư mục đầu vào!")
            return
        thread = threading.Thread(target=self.convert_batch_process)
        thread.daemon = True
        thread.start()

    def get_svg_dimensions(self, svg_content):
        try:
            root = ET.fromstring(svg_content)
            viewbox = root.get('viewBox')
            if viewbox:
                parts = viewbox.split()
                if len(parts) == 4: return float(parts[2]), float(parts[3])
            w = root.get('width', '100').replace('px', '').replace('pt', '')
            h = root.get('height', '100').replace('px', '').replace('pt', '')
            return float(w), float(h)
        except Exception: return 100.0, 100.0

    def extract_svg_content(self, svg_content):
        svg_start = svg_content.find('<svg')
        if svg_start == -1: return svg_content
        tag_end = svg_content.find('>', svg_start)
        if tag_end == -1: return svg_content
        svg_end = svg_content.rfind('</svg>')
        if svg_end == -1: return svg_content[tag_end + 1:].strip()
        return svg_content[tag_end + 1:svg_end].strip()

    def run_conversion(self, svg_file, png_file):
        out_w = int(self.width.get())
        out_h = int(self.height.get())
        margin_pct = float(self.margin_percent.get()) / 100.0
        bg = self.bg_color.get() or None

        with open(svg_file, 'r', encoding='utf-8') as f:
            svg_data = f.read()

        orig_w, orig_h = self.get_svg_dimensions(svg_data)
        margin_px_w = int(out_w * margin_pct)
        margin_px_h = int(out_h * margin_pct)
        icon_max_w = out_w - (2 * margin_px_w)
        icon_max_h = out_h - (2 * margin_px_h)
        scale = min(icon_max_w / orig_w, icon_max_h / orig_h)
        new_w, new_h = orig_w * scale, orig_h * scale
        x_offset = margin_px_w + (icon_max_w - new_w) / 2
        y_offset = margin_px_h + (icon_max_h - new_h) / 2
        inner_content = self.extract_svg_content(svg_data)
        
        wrapped_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{out_w}" height="{out_h}" viewBox="0 0 {out_w} {out_h}" xmlns="http://www.w3.org/2000/svg">
    {"<rect width='100%' height='100%' fill='" + bg + "' />" if bg else ""}
    <g transform="translate({x_offset:.2f}, {y_offset:.2f}) scale({scale:.4f})">
        {inner_content}
    </g>
</svg>'''
        cairosvg.svg2png(bytestring=wrapped_svg.encode('utf-8'), write_to=png_file, output_width=out_w, output_height=out_h)

    def convert_single_process(self):
        try:
            self.progress.start()
            self.status_label.config(text="Đang chuyển đổi...")
            self.run_conversion(self.svg_path.get(), self.output_path.get())
            self.status_label.config(text="Hoàn thành!")
            messagebox.showinfo("Thành công", f"Đã lưu: {self.output_path.get()}")
        except Exception as e:
            self.status_label.config(text="Lỗi!")
            messagebox.showerror("Lỗi", str(e))
        finally: self.progress.stop()

    def convert_batch_process(self):
        try:
            self.progress.start()
            in_dir = Path(self.batch_input_dir.get())
            out_dir = Path(self.batch_output_dir.get() or in_dir / "png_output")
            out_dir.mkdir(parents=True, exist_ok=True)
            
            svg_files = list(in_dir.glob("*.svg"))
            if not svg_files:
                messagebox.showwarning("Cảnh báo", "Không tìm thấy file SVG!")
                return
                
            total = len(svg_files)
            for i, svg_file in enumerate(svg_files):
                self.status_label.config(text=f"Đang xử lý {i+1}/{total}: {svg_file.name}")
                png_file = out_dir / f"{svg_file.stem}.png"
                self.run_conversion(str(svg_file), str(png_file))
                
            self.status_label.config(text=f"Hoàn thành {total} file!")
            messagebox.showinfo("Thành công", f"Đã chuyển đổi {total} file vào:\n{out_dir}")
        except Exception as e:
            self.status_label.config(text="Lỗi!")
            messagebox.showerror("Lỗi", str(e))
        finally: self.progress.stop()
