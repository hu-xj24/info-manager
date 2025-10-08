#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重要信息管理器
一个简单的GUI应用程序，用于存储和管理重要信息
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime
import threading


class InfoManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("重要信息管理器")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # 数据文件路径
        self.data_file = "important_info.json"
        
        # 存储信息的数据结构
        self.info_data = {
            "categories": {},
            "last_updated": ""
        }
        
        # 加载现有数据
        self.load_data()
        
        # 创建界面
        self.create_ui()
        
        # 设置窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_ui(self):
        """创建用户界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="重要信息管理器", 
                               font=("Microsoft YaHei", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 左侧面板 - 分类列表
        left_frame = ttk.LabelFrame(main_frame, text="分类", padding="5")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        left_frame.rowconfigure(1, weight=1)
        
        # 分类操作按钮
        category_btn_frame = ttk.Frame(left_frame)
        category_btn_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(category_btn_frame, text="添加分类", 
                  command=self.add_category).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(category_btn_frame, text="删除分类", 
                  command=self.delete_category).pack(side=tk.LEFT)
        
        # 分类列表
        self.category_listbox = tk.Listbox(left_frame, height=15)
        self.category_listbox.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.category_listbox.bind('<<ListboxSelect>>', self.on_category_select)
        
        # 分类列表滚动条
        category_scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, 
                                         command=self.category_listbox.yview)
        category_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.category_listbox.configure(yscrollcommand=category_scrollbar.set)
        
        # 中间面板 - 信息列表
        middle_frame = ttk.LabelFrame(main_frame, text="信息列表", padding="5")
        middle_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        middle_frame.rowconfigure(1, weight=1)
        
        # 信息操作按钮
        info_btn_frame = ttk.Frame(middle_frame)
        info_btn_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(info_btn_frame, text="添加信息", 
                  command=self.add_info).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(info_btn_frame, text="编辑信息", 
                  command=self.edit_info).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(info_btn_frame, text="删除信息", 
                  command=self.delete_info).pack(side=tk.LEFT)
        
        # 信息列表
        columns = ("标题", "内容", "创建时间")
        self.info_tree = ttk.Treeview(middle_frame, columns=columns, show="headings", height=15)
        
        # 设置列标题
        for col in columns:
            self.info_tree.heading(col, text=col)
            self.info_tree.column(col, width=150)
        
        self.info_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.info_tree.bind('<Double-1>', self.on_info_double_click)
        
        # 信息列表滚动条
        info_scrollbar = ttk.Scrollbar(middle_frame, orient=tk.VERTICAL, 
                                      command=self.info_tree.yview)
        info_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.info_tree.configure(yscrollcommand=info_scrollbar.set)
        
        # 右侧面板 - 详细信息
        right_frame = ttk.LabelFrame(main_frame, text="详细信息", padding="5")
        right_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.rowconfigure(2, weight=1)
        
        # 标题
        ttk.Label(right_frame, text="标题:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(right_frame, textvariable=self.title_var, width=30)
        self.title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # 内容
        ttk.Label(right_frame, text="内容:").grid(row=1, column=0, sticky=(tk.W, tk.N), pady=(0, 5))
        self.content_text = tk.Text(right_frame, width=30, height=10, wrap=tk.WORD)
        self.content_text.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 内容滚动条
        content_scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, 
                                         command=self.content_text.yview)
        content_scrollbar.grid(row=2, column=2, sticky=(tk.N, tk.S))
        self.content_text.configure(yscrollcommand=content_scrollbar.set)
        
        # 保存按钮
        ttk.Button(right_frame, text="保存", command=self.save_info).grid(row=3, column=0, columnspan=2, pady=10)
        
        # 底部状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 初始化显示
        self.refresh_category_list()
        self.current_category = None
    
    def load_data(self):
        """加载数据文件"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.info_data = json.load(f)
            else:
                self.info_data = {"categories": {}, "last_updated": ""}
        except Exception as e:
            messagebox.showerror("错误", f"加载数据文件失败: {str(e)}")
            self.info_data = {"categories": {}, "last_updated": ""}
    
    def save_data(self):
        """保存数据到文件"""
        try:
            self.info_data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.info_data, f, ensure_ascii=False, indent=2)
            self.status_var.set("数据已保存")
        except Exception as e:
            messagebox.showerror("错误", f"保存数据失败: {str(e)}")
    
    def refresh_category_list(self):
        """刷新分类列表"""
        self.category_listbox.delete(0, tk.END)
        for category in self.info_data["categories"].keys():
            self.category_listbox.insert(tk.END, category)
    
    def refresh_info_list(self, category):
        """刷新信息列表"""
        # 清空现有项目
        for item in self.info_tree.get_children():
            self.info_tree.delete(item)
        
        if category and category in self.info_data["categories"]:
            for info_id, info in self.info_data["categories"][category].items():
                # 使用iid参数设置唯一标识符
                self.info_tree.insert("", tk.END, iid=info_id, values=(
                    info.get("title", ""),
                    info.get("content", "")[:50] + "..." if len(info.get("content", "")) > 50 else info.get("content", ""),
                    info.get("created_time", "")
                ))
    
    def on_category_select(self, event):
        """分类选择事件"""
        selection = self.category_listbox.curselection()
        if selection:
            category = self.category_listbox.get(selection[0])
            self.current_category = category
            self.refresh_info_list(category)
            self.status_var.set(f"已选择分类: {category}")
    
    def on_info_double_click(self, event):
        """信息双击事件"""
        selection = self.info_tree.selection()
        if selection and self.current_category:
            info_id = selection[0]  # 直接使用iid作为info_id
            info = self.info_data["categories"][self.current_category][info_id]
            
            self.title_var.set(info.get("title", ""))
            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(1.0, info.get("content", ""))
    
    def add_category(self):
        """添加分类"""
        category = tk.simpledialog.askstring("添加分类", "请输入分类名称:")
        if category and category.strip():
            category = category.strip()
            if category not in self.info_data["categories"]:
                self.info_data["categories"][category] = {}
                self.refresh_category_list()
                self.save_data()
                self.status_var.set(f"已添加分类: {category}")
            else:
                messagebox.showwarning("警告", "分类已存在")
    
    def delete_category(self):
        """删除分类"""
        selection = self.category_listbox.curselection()
        if selection:
            category = self.category_listbox.get(selection[0])
            if messagebox.askyesno("确认删除", f"确定要删除分类 '{category}' 及其所有信息吗？"):
                del self.info_data["categories"][category]
                self.refresh_category_list()
                self.refresh_info_list(None)
                self.current_category = None
                self.title_var.set("")
                self.content_text.delete(1.0, tk.END)
                self.save_data()
                self.status_var.set(f"已删除分类: {category}")
        else:
            messagebox.showwarning("警告", "请先选择要删除的分类")
    
    def add_info(self):
        """添加信息"""
        if not self.current_category:
            messagebox.showwarning("警告", "请先选择一个分类")
            return
        
        # 清空输入框
        self.title_var.set("")
        self.content_text.delete(1.0, tk.END)
        self.status_var.set("请输入新信息")
    
    def edit_info(self):
        """编辑信息"""
        selection = self.info_tree.selection()
        if selection and self.current_category:
            self.on_info_double_click(None)
            self.status_var.set("正在编辑信息")
        else:
            messagebox.showwarning("警告", "请先选择要编辑的信息")
    
    def delete_info(self):
        """删除信息"""
        selection = self.info_tree.selection()
        if selection and self.current_category:
            info_id = selection[0]  # 直接使用iid作为info_id
            item = self.info_tree.item(selection[0])
            info_title = item['values'][0]
            
            if messagebox.askyesno("确认删除", f"确定要删除信息 '{info_title}' 吗？"):
                del self.info_data["categories"][self.current_category][info_id]
                self.refresh_info_list(self.current_category)
                self.title_var.set("")
                self.content_text.delete(1.0, tk.END)
                self.save_data()
                self.status_var.set(f"已删除信息: {info_title}")
        else:
            messagebox.showwarning("警告", "请先选择要删除的信息")
    
    def save_info(self):
        """保存信息"""
        if not self.current_category:
            messagebox.showwarning("警告", "请先选择一个分类")
            return
        
        title = self.title_var.get().strip()
        content = self.content_text.get(1.0, tk.END).strip()
        
        if not title:
            messagebox.showwarning("警告", "请输入标题")
            return
        
        if not content:
            messagebox.showwarning("警告", "请输入内容")
            return
        
        # 生成唯一ID
        info_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        
        # 保存信息
        self.info_data["categories"][self.current_category][info_id] = {
            "title": title,
            "content": content,
            "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.refresh_info_list(self.current_category)
        self.save_data()
        self.status_var.set(f"已保存信息: {title}")
    
    def on_closing(self):
        """窗口关闭事件"""
        self.save_data()
        self.root.destroy()
    
    def run(self):
        """运行应用程序"""
        self.root.mainloop()


if __name__ == "__main__":
    # 导入simpledialog模块
    import tkinter.simpledialog
    
    app = InfoManager()
    app.run()
