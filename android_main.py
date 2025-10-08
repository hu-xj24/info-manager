#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重要信息管理器 - Android版本
使用Kivy框架开发的移动端应用
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.listview import ListView, ListItemButton
from kivy.adapters.listadapter import ListAdapter
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
import json
import os
from datetime import datetime


class CategoryScreen(Screen):
    """分类管理界面"""
    
    def __init__(self, **kwargs):
        super(CategoryScreen, self).__init__(**kwargs)
        self.data_manager = App.get_running_app().data_manager
        
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        title = Label(text='分类管理', size_hint_y=0.1, font_size=24)
        main_layout.add_widget(title)
        
        # 分类列表
        self.category_list = ListView(size_hint_y=0.7)
        main_layout.add_widget(self.category_list)
        
        # 按钮区域
        button_layout = BoxLayout(size_hint_y=0.2, spacing=10)
        
        add_btn = Button(text='添加分类')
        add_btn.bind(on_press=self.add_category)
        button_layout.add_widget(add_btn)
        
        delete_btn = Button(text='删除分类')
        delete_btn.bind(on_press=self.delete_category)
        button_layout.add_widget(delete_btn)
        
        main_layout.add_widget(button_layout)
        
        self.add_widget(main_layout)
        self.refresh_list()
    
    def refresh_list(self):
        """刷新分类列表"""
        categories = list(self.data_manager.get_categories().keys())
        self.category_list.adapter = ListAdapter(
            data=categories,
            cls=ListItemButton,
            selection_mode='single'
        )
    
    def add_category(self, instance):
        """添加分类"""
        content = BoxLayout(orientation='vertical', spacing=10)
        text_input = TextInput(hint_text='请输入分类名称', multiline=False)
        content.add_widget(text_input)
        
        btn_layout = BoxLayout(size_hint_y=0.3, spacing=10)
        ok_btn = Button(text='确定')
        cancel_btn = Button(text='取消')
        
        popup = Popup(title='添加分类', content=content, size_hint=(0.8, 0.4))
        
        def on_ok(instance):
            category_name = text_input.text.strip()
            if category_name:
                self.data_manager.add_category(category_name)
                self.refresh_list()
                popup.dismiss()
        
        ok_btn.bind(on_press=on_ok)
        cancel_btn.bind(on_press=popup.dismiss)
        
        btn_layout.add_widget(ok_btn)
        btn_layout.add_widget(cancel_btn)
        content.add_widget(btn_layout)
        
        popup.open()
    
    def delete_category(self, instance):
        """删除分类"""
        if self.category_list.adapter.selection:
            category = self.category_list.adapter.selection[0].text
            self.data_manager.delete_category(category)
            self.refresh_list()


class InfoScreen(Screen):
    """信息管理界面"""
    
    def __init__(self, **kwargs):
        super(InfoScreen, self).__init__(**kwargs)
        self.data_manager = App.get_running_app().data_manager
        self.current_category = None
        
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        title = Label(text='信息管理', size_hint_y=0.1, font_size=24)
        main_layout.add_widget(title)
        
        # 分类选择
        category_layout = BoxLayout(size_hint_y=0.1, spacing=10)
        category_layout.add_widget(Label(text='选择分类:', size_hint_x=0.3))
        
        self.category_spinner = Button(text='请选择分类', size_hint_x=0.7)
        self.category_spinner.bind(on_press=self.select_category)
        category_layout.add_widget(self.category_spinner)
        
        main_layout.add_widget(category_layout)
        
        # 信息列表
        self.info_list = ListView(size_hint_y=0.5)
        main_layout.add_widget(self.info_list)
        
        # 按钮区域
        button_layout = BoxLayout(size_hint_y=0.1, spacing=10)
        
        add_btn = Button(text='添加信息')
        add_btn.bind(on_press=self.add_info)
        button_layout.add_widget(add_btn)
        
        edit_btn = Button(text='编辑信息')
        edit_btn.bind(on_press=self.edit_info)
        button_layout.add_widget(edit_btn)
        
        delete_btn = Button(text='删除信息')
        delete_btn.bind(on_press=self.delete_info)
        button_layout.add_widget(delete_btn)
        
        main_layout.add_widget(button_layout)
        
        self.add_widget(main_layout)
    
    def select_category(self, instance):
        """选择分类"""
        categories = list(self.data_manager.get_categories().keys())
        if not categories:
            return
        
        content = BoxLayout(orientation='vertical', spacing=10)
        list_view = ListView(size_hint_y=0.7)
        
        adapter = ListAdapter(
            data=categories,
            cls=ListItemButton,
            selection_mode='single'
        )
        list_view.adapter = adapter
        
        content.add_widget(list_view)
        
        btn_layout = BoxLayout(size_hint_y=0.3, spacing=10)
        ok_btn = Button(text='确定')
        cancel_btn = Button(text='取消')
        
        popup = Popup(title='选择分类', content=content, size_hint=(0.8, 0.6))
        
        def on_ok(instance):
            if adapter.selection:
                self.current_category = adapter.selection[0].text
                self.category_spinner.text = self.current_category
                self.refresh_info_list()
                popup.dismiss()
        
        ok_btn.bind(on_press=on_ok)
        cancel_btn.bind(on_press=popup.dismiss)
        
        btn_layout.add_widget(ok_btn)
        btn_layout.add_widget(cancel_btn)
        content.add_widget(btn_layout)
        
        popup.open()
    
    def refresh_info_list(self):
        """刷新信息列表"""
        if not self.current_category:
            return
        
        infos = self.data_manager.get_infos(self.current_category)
        info_list = []
        for info_id, info in infos.items():
            info_list.append(f"{info['title']} - {info['created_time']}")
        
        self.info_list.adapter = ListAdapter(
            data=info_list,
            cls=ListItemButton,
            selection_mode='single'
        )
    
    def add_info(self, instance):
        """添加信息"""
        if not self.current_category:
            return
        
        self.show_info_dialog()
    
    def edit_info(self, instance):
        """编辑信息"""
        if not self.current_category or not self.info_list.adapter.selection:
            return
        
        # 获取选中的信息
        selected_text = self.info_list.adapter.selection[0].text
        # 这里需要根据实际需求实现编辑逻辑
        self.show_info_dialog()
    
    def delete_info(self, instance):
        """删除信息"""
        if not self.current_category or not self.info_list.adapter.selection:
            return
        
        # 实现删除逻辑
        self.refresh_info_list()
    
    def show_info_dialog(self):
        """显示信息编辑对话框"""
        content = BoxLayout(orientation='vertical', spacing=10)
        
        title_input = TextInput(hint_text='请输入标题', multiline=False, size_hint_y=0.2)
        content_input = TextInput(hint_text='请输入内容', multiline=True, size_hint_y=0.6)
        
        content.add_widget(title_input)
        content.add_widget(content_input)
        
        btn_layout = BoxLayout(size_hint_y=0.2, spacing=10)
        ok_btn = Button(text='保存')
        cancel_btn = Button(text='取消')
        
        popup = Popup(title='编辑信息', content=content, size_hint=(0.9, 0.8))
        
        def on_ok(instance):
            title = title_input.text.strip()
            content_text = content_input.text.strip()
            if title and content_text:
                self.data_manager.add_info(self.current_category, title, content_text)
                self.refresh_info_list()
                popup.dismiss()
        
        ok_btn.bind(on_press=on_ok)
        cancel_btn.bind(on_press=popup.dismiss)
        
        btn_layout.add_widget(ok_btn)
        btn_layout.add_widget(cancel_btn)
        content.add_widget(btn_layout)
        
        popup.open()


class DataManager:
    """数据管理器"""
    
    def __init__(self):
        self.store = JsonStore('important_info.json')
        self.init_data()
    
    def init_data(self):
        """初始化数据"""
        if not self.store.exists('categories'):
            self.store.put('categories', data={})
    
    def get_categories(self):
        """获取所有分类"""
        return self.store.get('categories')['data']
    
    def add_category(self, category_name):
        """添加分类"""
        categories = self.get_categories()
        categories[category_name] = {}
        self.store.put('categories', data=categories)
    
    def delete_category(self, category_name):
        """删除分类"""
        categories = self.get_categories()
        if category_name in categories:
            del categories[category_name]
            self.store.put('categories', data=categories)
    
    def get_infos(self, category):
        """获取分类下的所有信息"""
        categories = self.get_categories()
        return categories.get(category, {})
    
    def add_info(self, category, title, content):
        """添加信息"""
        categories = self.get_categories()
        if category not in categories:
            categories[category] = {}
        
        info_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        categories[category][info_id] = {
            'title': title,
            'content': content,
            'created_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.store.put('categories', data=categories)


class InfoManagerApp(App):
    """主应用程序"""
    
    def build(self):
        self.data_manager = DataManager()
        
        # 创建屏幕管理器
        sm = ScreenManager()
        
        # 添加分类管理屏幕
        category_screen = CategoryScreen(name='category')
        sm.add_widget(category_screen)
        
        # 添加信息管理屏幕
        info_screen = InfoScreen(name='info')
        sm.add_widget(info_screen)
        
        # 创建标签面板
        tab_panel = TabbedPanel(do_default_tab=False)
        
        # 分类管理标签
        category_tab = TabbedPanelItem(text='分类管理')
        category_tab.add_widget(category_screen)
        tab_panel.add_widget(category_tab)
        
        # 信息管理标签
        info_tab = TabbedPanelItem(text='信息管理')
        info_tab.add_widget(info_screen)
        tab_panel.add_widget(info_tab)
        
        return tab_panel


if __name__ == '__main__':
    InfoManagerApp().run()
