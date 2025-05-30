# -*- coding: utf-8 -*-
"""
记忆管理界面组件
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QListWidget, QListWidgetItem,
                             QTextEdit, QLineEdit, QComboBox, QSpinBox,
                             QDialog, QDialogButtonBox, QMessageBox,
                             QFrame, QScrollArea, QGroupBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from datetime import datetime


class MemoryItemWidget(QFrame):
    """记忆项组件"""
    
    edit_requested = pyqtSignal(object)  # 发送记忆项对象
    delete_requested = pyqtSignal(object)  # 发送记忆项对象
    
    def __init__(self, memory_item, is_dark_theme=False):
        super().__init__()
        self.memory_item = memory_item
        self.is_dark_theme = is_dark_theme
        
        # 设置固定尺寸约束
        self.setMaximumWidth(320)
        self.setMaximumHeight(120)
        
        self.init_ui()
        self.set_style()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(5)
        
        # 顶部信息行
        top_layout = QHBoxLayout()
        
        # 类别标签
        self.category_label = QLabel(self.memory_item.category)
        top_layout.addWidget(self.category_label)
        
        # 重要性显示
        importance_text = "★" * self.memory_item.importance
        self.importance_label = QLabel(importance_text)
        top_layout.addWidget(self.importance_label)
        
        top_layout.addStretch()
        
        # 时间戳
        time_str = datetime.fromisoformat(self.memory_item.timestamp).strftime("%m-%d %H:%M")
        self.time_label = QLabel(time_str)
        top_layout.addWidget(self.time_label)
        
        layout.addLayout(top_layout)
        
        # 记忆内容
        content_text = self.memory_item.content
        # 限制显示长度，避免撑大布局
        if len(content_text) > 80:
            content_text = content_text[:80] + "..."
        
        self.content_label = QLabel(content_text)
        self.content_label.setWordWrap(True)
        self.content_label.setMaximumHeight(50)  # 限制高度
        self.content_label.setAlignment(Qt.AlignTop)
        layout.addWidget(self.content_label)
        
        # 操作按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.edit_btn = QPushButton("编辑")
        self.edit_btn.setFixedSize(50, 25)
        self.edit_btn.clicked.connect(lambda: self.edit_requested.emit(self.memory_item))
        
        self.delete_btn = QPushButton("删除")
        self.delete_btn.setFixedSize(50, 25)
        self.delete_btn.clicked.connect(lambda: self.delete_requested.emit(self.memory_item))
        
        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.delete_btn)
        
        layout.addLayout(button_layout)
    
    def set_style(self):
        """设置样式"""
        if self.is_dark_theme:
            # 深色主题
            frame_style = """
            QFrame {
                background-color: #363636;
                border: 1px solid #555555;
                border-radius: 8px;
                margin: 2px;
            }
            QFrame:hover {
                border-color: #007acc;
                background-color: #404040;
            }
            """
            
            category_style = """
            QLabel {
                background-color: #007acc;
                color: white;
                padding: 2px 8px;
                border-radius: 10px;
                font-size: 10px;
                font-weight: bold;
            }
            """
            
            button_style = """
            QPushButton {
                background-color: #505050;
                border: 1px solid #666666;
                border-radius: 12px;
                font-size: 10px;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #606060;
            }
            """
            
            self.importance_label.setStyleSheet("color: #ffa500; font-size: 12px;")
            self.time_label.setStyleSheet("color: #bbbbbb; font-size: 10px;")
            self.content_label.setStyleSheet("color: #ffffff; font-size: 11px; margin: 5px 0;")
        else:
            # 浅色主题
            frame_style = """
            QFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                margin: 2px;
            }
            QFrame:hover {
                border-color: #007acc;
                background-color: #f8f9ff;
            }
            """
            
            category_style = """
            QLabel {
                background-color: #007acc;
                color: white;
                padding: 2px 8px;
                border-radius: 10px;
                font-size: 10px;
                font-weight: bold;
            }
            """
            
            button_style = """
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 12px;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            """
            
            self.importance_label.setStyleSheet("color: #ffa500; font-size: 12px;")
            self.time_label.setStyleSheet("color: #888; font-size: 10px;")
            self.content_label.setStyleSheet("color: #333; font-size: 11px; margin: 5px 0;")
        
        self.setStyleSheet(frame_style)
        self.category_label.setStyleSheet(category_style)
        self.edit_btn.setStyleSheet(button_style)
        self.delete_btn.setStyleSheet(button_style)
    
    def set_theme(self, is_dark_theme: bool):
        """设置主题"""
        self.is_dark_theme = is_dark_theme
        self.set_style()


class MemoryEditDialog(QDialog):
    """记忆编辑对话框"""
    
    def __init__(self, memory_item=None, parent=None, is_dark_theme=False):
        super().__init__(parent)
        self.memory_item = memory_item
        self.is_new = memory_item is None
        self.is_dark_theme = is_dark_theme
        
        self.init_ui()
        if not self.is_new:
            self.load_memory_data()
        self.set_style()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("编辑记忆" if not self.is_new else "添加记忆")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # 记忆内容
        layout.addWidget(QLabel("记忆内容:"))
        self.content_edit = QTextEdit()
        self.content_edit.setFixedHeight(100)
        layout.addWidget(self.content_edit)
        
        # 类别选择
        layout.addWidget(QLabel("类别:"))
        self.category_combo = QComboBox()
        self.category_combo.addItems(["个人信息", "喜好", "情感", "重要事件", "general"])
        layout.addWidget(self.category_combo)
        
        # 重要性
        layout.addWidget(QLabel("重要性 (1-5):"))
        self.importance_spin = QSpinBox()
        self.importance_spin.setRange(1, 5)
        self.importance_spin.setValue(1)
        layout.addWidget(self.importance_spin)
        
        # 按钮
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def load_memory_data(self):
        """加载记忆数据"""
        if self.memory_item:
            self.content_edit.setPlainText(self.memory_item.content)
            
            # 设置类别
            index = self.category_combo.findText(self.memory_item.category)
            if index >= 0:
                self.category_combo.setCurrentIndex(index)
            
            self.importance_spin.setValue(self.memory_item.importance)
    
    def get_memory_data(self):
        """获取记忆数据"""
        return {
            'content': self.content_edit.toPlainText().strip(),
            'category': self.category_combo.currentText(),
            'importance': self.importance_spin.value()
        }

    def set_style(self):
        """设置样式"""
        if self.is_dark_theme:
            style = """
            QDialog {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QTextEdit {
                background-color: #363636;
                border: 1px solid #555555;
                color: #ffffff;
                border-radius: 3px;
                padding: 4px;
            }
            QComboBox {
                background-color: #363636;
                border: 1px solid #555555;
                color: #ffffff;
                padding: 4px;
                border-radius: 3px;
            }
            QComboBox::drop-down {
                border: none;
                background-color: #505050;
            }
            QComboBox::down-arrow {
                image: none;
                border-style: solid;
                border-width: 3px;
                border-color: #ffffff transparent transparent transparent;
            }
            QComboBox QAbstractItemView {
                background-color: #363636;
                color: #ffffff;
                selection-background-color: #007acc;
            }
            QSpinBox {
                background-color: #363636;
                border: 1px solid #555555;
                color: #ffffff;
                padding: 4px;
                border-radius: 3px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #505050;
                border: 1px solid #666666;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #606060;
            }
            QDialogButtonBox QPushButton {
                background-color: #505050;
                border: 1px solid #666666;
                padding: 6px 12px;
                border-radius: 3px;
                color: #ffffff;
                min-width: 60px;
            }
            QDialogButtonBox QPushButton:hover {
                background-color: #606060;
            }
            QDialogButtonBox QPushButton:default {
                background-color: #007acc;
            }
            QDialogButtonBox QPushButton:default:hover {
                background-color: #005a9e;
            }
            """
        else:
            style = """
            QDialog {
                background-color: #ffffff;
                color: #333333;
            }
            """
        
        self.setStyleSheet(style)


class MemoryWidget(QWidget):
    """记忆管理组件"""
    
    memory_updated = pyqtSignal()  # 记忆更新信号
    
    def __init__(self, chat_engine):
        super().__init__()
        self.chat_engine = chat_engine
        self.memory_items = []
        self.is_dark_theme = False
        
        self.init_ui()
        self.refresh_memories()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # 创建各个部分
        self.create_header()
        layout.addWidget(self.header_frame)
        
        self.create_search_panel()
        layout.addWidget(self.search_frame)
        
        self.create_memory_list()
        layout.addWidget(self.memory_scroll)
        
        self.create_action_buttons()
        layout.addWidget(self.button_frame)
        
        # 设置样式
        self.set_style()
    
    def set_style(self):
        """设置样式"""
        if self.is_dark_theme:
            # 深色主题样式
            main_style = """
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QFrame {
                background-color: #363636;
                border: 1px solid #555555;
                border-radius: 5px;
            }
            QScrollArea {
                background-color: #2b2b2b;
                border: 1px solid #555555;
            }
            QLineEdit {
                background-color: #363636;
                border: 1px solid #555555;
                padding: 4px;
                border-radius: 3px;
                color: #ffffff;
            }
            QLineEdit:focus {
                border-color: #007acc;
            }
            QComboBox {
                background-color: #363636;
                border: 1px solid #555555;
                padding: 4px;
                border-radius: 3px;
                color: #ffffff;
            }
            QComboBox::drop-down {
                background-color: #505050;
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-style: solid;
                border-width: 3px;
                border-color: #ffffff transparent transparent transparent;
            }
            QComboBox QAbstractItemView {
                background-color: #363636;
                color: #ffffff;
                selection-background-color: #007acc;
            }
            QPushButton {
                background-color: #505050;
                border: 1px solid #666666;
                padding: 6px 12px;
                border-radius: 3px;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #606060;
            }
            QPushButton:pressed {
                background-color: #404040;
            }
            QLabel {
                color: #ffffff;
            }
            /* 滚动条样式 */
            QScrollBar:vertical {
                background-color: #2b2b2b;
                width: 12px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background-color: #555555;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #666666;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background-color: transparent;
            }
            QScrollBar:horizontal {
                background-color: #2b2b2b;
                height: 12px;
                border: none;
            }
            QScrollBar::handle:horizontal {
                background-color: #555555;
                border-radius: 6px;
                min-width: 20px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #666666;
            }
            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                width: 0px;
            }
            QScrollBar::add-page:horizontal,
            QScrollBar::sub-page:horizontal {
                background-color: transparent;
            }
            """
            
            # 设置统计标签样式
            self.stats_label.setStyleSheet("color: #bbbbbb; font-size: 11px;")
        else:
            # 浅色主题样式
            main_style = """
            QWidget {
                background-color: #ffffff;
                color: #333333;
            }
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
            }
            QScrollArea {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
            }
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #ddd;
                padding: 4px;
                border-radius: 3px;
            }
            QComboBox {
                background-color: #ffffff;
                border: 1px solid #ddd;
                padding: 4px;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                padding: 6px 12px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
            """
            
            # 设置统计标签样式
            self.stats_label.setStyleSheet("color: #666; font-size: 11px;")
        
        self.setStyleSheet(main_style)
    
    def set_theme(self, is_dark_theme: bool):
        """设置主题"""
        self.is_dark_theme = is_dark_theme
        self.set_style()
        
        # 更新内存项的主题
        self.update_memory_display()
    
    def create_header(self):
        """创建头部信息"""
        self.header_frame = QFrame()
        layout = QVBoxLayout(self.header_frame)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 标题
        self.title_label = QLabel("记忆管理")
        try:
            from utils.helpers import get_system_font
            title_font = get_system_font(14, bold=True)
            if title_font:
                self.title_label.setFont(title_font)
        except ImportError:
            title_font = QFont()
            title_font.setPointSize(14)
            title_font.setBold(True)
            self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)
        
        # 统计信息
        self.stats_label = QLabel("记忆统计信息")
        self.stats_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.stats_label)
    
    def create_search_panel(self):
        """创建搜索面板"""
        self.search_frame = QFrame()
        layout = QHBoxLayout(self.search_frame)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # 搜索框
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("搜索记忆内容...")
        self.search_edit.textChanged.connect(self.on_search_changed)
        layout.addWidget(self.search_edit)
        
        # 类别过滤
        self.category_filter = QComboBox()
        self.category_filter.addItems(["全部", "个人信息", "喜好", "情感", "重要事件", "general"])
        self.category_filter.currentTextChanged.connect(self.on_filter_changed)
        layout.addWidget(self.category_filter)
    
    def create_memory_list(self):
        """创建记忆列表"""
        self.memory_scroll = QScrollArea()
        self.memory_scroll.setWidgetResizable(True)
        self.memory_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.memory_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        self.memory_container = QWidget()
        # 设置容器固定宽度，防止撑大左边栏
        self.memory_container.setMaximumWidth(320)
        
        self.memory_layout = QVBoxLayout(self.memory_container)
        self.memory_layout.setContentsMargins(0, 0, 0, 0)
        self.memory_layout.setSpacing(5)
        self.memory_layout.addStretch()
        
        self.memory_scroll.setWidget(self.memory_container)
    
    def create_action_buttons(self):
        """创建操作按钮"""
        self.button_frame = QFrame()
        layout = QHBoxLayout(self.button_frame)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # 添加记忆按钮
        add_btn = QPushButton("添加记忆")
        add_btn.clicked.connect(self.add_memory)
        layout.addWidget(add_btn)
        
        layout.addStretch()
        
        # 刷新按钮
        refresh_btn = QPushButton("刷新")
        refresh_btn.clicked.connect(self.refresh_memories)
        layout.addWidget(refresh_btn)
        
        # 清空记忆按钮
        clear_btn = QPushButton("清空记忆")
        clear_btn.clicked.connect(self.clear_memories)
        layout.addWidget(clear_btn)
    
    def refresh_memories(self):
        """刷新记忆列表"""
        personality_id = self.chat_engine.personality_manager.get_current_personality_id()
        if not personality_id:
            return
        
        # 获取记忆列表
        self.memory_items = self.chat_engine.memory_manager.get_memories(personality_id)
        
        # 更新统计信息
        self.update_stats()
        
        # 更新记忆显示
        self.update_memory_display()
    
    def update_stats(self):
        """更新统计信息"""
        summary = self.chat_engine.get_memory_summary()
        total_count = summary['total_count']
        category_stats = summary['category_stats']
        
        stats_text = f"总记忆数: {total_count}"
        if category_stats:
            category_text = ", ".join([f"{cat}: {count}" for cat, count in category_stats.items()])
            stats_text += f" | 分类: {category_text}"
        
        self.stats_label.setText(stats_text)
    
    def update_memory_display(self):
        """更新记忆显示"""
        # 清除现有记忆项（保留弹性空间）
        while self.memory_layout.count() > 1:  # 保留最后的弹性空间
            item = self.memory_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # 应用搜索和过滤
        filtered_memories = self.filter_memories()
        
        # 添加记忆项
        for memory in filtered_memories:
            memory_widget = MemoryItemWidget(memory, self.is_dark_theme)
            memory_widget.edit_requested.connect(self.edit_memory)
            memory_widget.delete_requested.connect(self.delete_memory)
            
            # 在弹性空间之前插入记忆项
            self.memory_layout.insertWidget(self.memory_layout.count() - 1, memory_widget)
        
        # 如果没有记忆，显示提示
        if not filtered_memories:
            no_memory_label = QLabel("暂无记忆数据")
            no_memory_label.setAlignment(Qt.AlignCenter)
            
            # 根据主题设置样式
            if self.is_dark_theme:
                no_memory_label.setStyleSheet("color: #bbbbbb; font-size: 12px; padding: 20px;")
            else:
                no_memory_label.setStyleSheet("color: #888; font-size: 12px; padding: 20px;")
            
            # 在弹性空间之前插入提示标签
            self.memory_layout.insertWidget(self.memory_layout.count() - 1, no_memory_label)
    
    def filter_memories(self):
        """过滤记忆"""
        search_text = self.search_edit.text().lower()
        category_filter = self.category_filter.currentText()
        
        filtered = []
        for memory in self.memory_items:
            # 搜索过滤
            if search_text and search_text not in memory.content.lower():
                continue
            
            # 类别过滤
            if category_filter != "全部" and memory.category != category_filter:
                continue
            
            filtered.append(memory)
        
        return filtered
    
    def on_search_changed(self):
        """搜索文本改变"""
        self.update_memory_display()
    
    def on_filter_changed(self):
        """过滤条件改变"""
        self.update_memory_display()
    
    def add_memory(self):
        """添加记忆"""
        dialog = MemoryEditDialog(parent=self, is_dark_theme=self.is_dark_theme)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_memory_data()
            if data['content']:
                from ai.memory import MemoryItem
                memory_item = MemoryItem(
                    content=data['content'],
                    category=data['category'],
                    importance=data['importance']
                )
                
                personality_id = self.chat_engine.personality_manager.get_current_personality_id()
                if personality_id:
                    success = self.chat_engine.memory_manager.add_memory(personality_id, memory_item)
                    if success:
                        self.refresh_memories()
                        self.memory_updated.emit()
                    else:
                        QMessageBox.warning(self, "错误", "添加记忆失败")
    
    def edit_memory(self, memory_item):
        """编辑记忆"""
        dialog = MemoryEditDialog(memory_item, parent=self, is_dark_theme=self.is_dark_theme)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_memory_data()
            if data['content']:
                success = self.chat_engine.memory_manager.update_memory(
                    memory_item.id,
                    content=data['content'],
                    category=data['category'],
                    importance=data['importance']
                )
                if success:
                    self.refresh_memories()
                    self.memory_updated.emit()
                else:
                    QMessageBox.warning(self, "错误", "更新记忆失败")
    
    def delete_memory(self, memory_item):
        """删除记忆"""
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除这条记忆吗？\n\n{memory_item.content[:50]}...",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success = self.chat_engine.memory_manager.delete_memory(memory_item.id)
            if success:
                self.refresh_memories()
                self.memory_updated.emit()
            else:
                QMessageBox.warning(self, "错误", "删除记忆失败")
    
    def clear_memories(self):
        """清空记忆"""
        reply = QMessageBox.question(
            self, "确认清空",
            "确定要清空当前人格的所有记忆吗？此操作不可恢复！",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            personality_id = self.chat_engine.personality_manager.get_current_personality_id()
            if personality_id:
                # 删除所有记忆
                for memory in self.memory_items:
                    self.chat_engine.memory_manager.delete_memory(memory.id)
                
                self.refresh_memories()
                self.memory_updated.emit()
                QMessageBox.information(self, "完成", "记忆已清空") 