# -*- coding: utf-8 -*-
"""
人格选择界面组件
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QButtonGroup, QRadioButton,
                             QTextEdit, QFrame, QScrollArea)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPalette


class PersonalityCard(QFrame):
    """人格卡片"""
    
    clicked = pyqtSignal(str)  # 发送人格ID
    
    def __init__(self, personality_id: str, personality_data: dict, is_dark_theme: bool = False):
        super().__init__()
        self.personality_id = personality_id
        self.personality_data = personality_data
        self.is_selected = False
        self.is_dark_theme = is_dark_theme
        
        self.init_ui()
        self.set_style()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)
        
        # 人格名称
        self.name_label = QLabel(self.personality_data.get('name', self.personality_id))
        # 使用系统兼容的字体
        try:
            from utils.helpers import get_system_font
            name_font = get_system_font(12, bold=True)
            if name_font:
                self.name_label.setFont(name_font)
        except ImportError:
            # 如果导入失败，使用默认字体
            name_font = QFont()
            name_font.setPointSize(12)
            name_font.setBold(True)
            self.name_label.setFont(name_font)
        layout.addWidget(self.name_label)
        
        # 人格描述
        self.desc_label = QLabel(self.personality_data.get('description', ''))
        self.desc_label.setWordWrap(True)
        layout.addWidget(self.desc_label)
        
        # 人格特征
        traits = self.personality_data.get('personality_traits', [])
        if traits:
            traits_text = "特征: " + ", ".join(traits)
            self.traits_label = QLabel(traits_text)
            self.traits_label.setWordWrap(True)
            layout.addWidget(self.traits_label)
        else:
            self.traits_label = None
        
        # 设置固定高度
        self.setFixedHeight(120)
    
    def set_style(self):
        """设置样式"""
        self.set_selected(self.is_selected)
        self.update_label_colors()
    
    def update_label_colors(self):
        """更新标签颜色"""
        if self.is_dark_theme:
            desc_color = "#bbbbbb"
            traits_color = "#999999"
        else:
            desc_color = "#666666"
            traits_color = "#888888"
        
        self.desc_label.setStyleSheet(f"color: {desc_color}; font-size: 11px;")
        if self.traits_label:
            self.traits_label.setStyleSheet(f"color: {traits_color}; font-size: 10px; font-style: italic;")
    
    def set_selected(self, selected: bool):
        """设置选中状态"""
        self.is_selected = selected
        
        if self.is_dark_theme:
            if selected:
                style = """
                QFrame {
                    background-color: #003d66;
                    border: 2px solid #007acc;
                    border-radius: 10px;
                    margin: 2px;
                }
                """
            else:
                style = """
                QFrame {
                    background-color: #363636;
                    border: 2px solid #555555;
                    border-radius: 10px;
                    margin: 2px;
                }
                QFrame:hover {
                    border-color: #007acc;
                    background-color: #404040;
                }
                """
        else:
            if selected:
                style = """
                QFrame {
                    background-color: #e6f3ff;
                    border: 2px solid #007acc;
                    border-radius: 10px;
                    margin: 2px;
                }
                """
            else:
                style = """
                QFrame {
                    background-color: white;
                    border: 2px solid #e0e0e0;
                    border-radius: 10px;
                    margin: 2px;
                }
                QFrame:hover {
                    border-color: #007acc;
                    background-color: #f8f9ff;
                }
                """
        self.setStyleSheet(style)
    
    def set_theme(self, is_dark_theme: bool):
        """设置主题"""
        self.is_dark_theme = is_dark_theme
        self.set_style()
    
    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.personality_id)
        super().mousePressEvent(event)


class PersonalityWidget(QWidget):
    """人格选择组件"""
    
    personality_changed = pyqtSignal(str)  # 发送新的人格ID
    
    def __init__(self, chat_engine):
        super().__init__()
        self.chat_engine = chat_engine
        self.personality_cards = {}
        self.current_personality_id = None
        self.is_dark_theme = False
        
        self.init_ui()
        self.load_personalities()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # 标题
        self.title_label = QLabel("选择AI人格")
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
        
        # 说明文字
        self.desc_label = QLabel("不同的人格会展现不同的对话风格和记忆关注点")
        self.desc_label.setWordWrap(True)
        self.desc_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.desc_label)
        
        # 滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # 人格卡片容器
        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(10)
        self.cards_layout.addStretch()  # 添加弹性空间
        
        self.scroll_area.setWidget(self.cards_container)
        layout.addWidget(self.scroll_area)
        
        # 当前人格信息显示
        self.create_current_info_panel()
        layout.addWidget(self.current_info_frame)
        
        # 设置样式
        self.set_style()
    
    def create_current_info_panel(self):
        """创建当前人格信息面板"""
        self.current_info_frame = QFrame()
        self.current_info_frame.setFixedHeight(100)
        
        layout = QVBoxLayout(self.current_info_frame)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 标题
        self.info_title = QLabel("当前人格")
        try:
            from utils.helpers import get_system_font
            info_font = get_system_font(11, bold=True)
            if info_font:
                self.info_title.setFont(info_font)
        except ImportError:
            info_font = QFont()
            info_font.setPointSize(11)
            info_font.setBold(True)
            self.info_title.setFont(info_font)
        layout.addWidget(self.info_title)
        
        # 当前人格信息
        self.current_info_label = QLabel("未选择人格")
        self.current_info_label.setWordWrap(True)
        layout.addWidget(self.current_info_label)
    
    def set_style(self):
        """设置样式"""
        if self.is_dark_theme:
            # 深色主题
            desc_style = "color: #bbbbbb; font-size: 11px; margin-bottom: 10px;"
            scroll_style = """
            QScrollArea {
                background-color: #2b2b2b;
                border: 1px solid #404040;
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
            """
            frame_style = """
            QFrame {
                background-color: #363636;
                border: 1px solid #555555;
                border-radius: 5px;
            }
            """
            info_style = "color: #cccccc; font-size: 11px;"
        else:
            # 浅色主题
            desc_style = "color: #666; font-size: 11px; margin-bottom: 10px;"
            scroll_style = """
            QScrollArea {
                background-color: white;
                border: 1px solid #e0e0e0;
            }
            """
            frame_style = """
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
            }
            """
            info_style = "color: #666; font-size: 11px;"
        
        self.desc_label.setStyleSheet(desc_style)
        self.scroll_area.setStyleSheet(scroll_style)
        self.current_info_frame.setStyleSheet(frame_style)
        self.current_info_label.setStyleSheet(info_style)
    
    def set_theme(self, is_dark_theme: bool):
        """设置主题"""
        self.is_dark_theme = is_dark_theme
        self.set_style()
        
        # 更新所有人格卡片的主题
        for card in self.personality_cards.values():
            card.set_theme(is_dark_theme)
    
    def load_personalities(self):
        """加载人格列表"""
        personalities = self.chat_engine.personality_manager.get_personalities()
        current_id = self.chat_engine.personality_manager.get_current_personality_id()
        
        # 清除现有的卡片（保留弹性空间）
        while self.cards_layout.count() > 1:  # 保留最后的弹性空间
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # 创建人格卡片
        for personality_id, personality_data in personalities.items():
            card = PersonalityCard(personality_id, personality_data, self.is_dark_theme)
            card.clicked.connect(self.on_personality_selected)
            
            self.personality_cards[personality_id] = card
            
            # 在弹性空间之前插入卡片
            self.cards_layout.insertWidget(self.cards_layout.count() - 1, card)
            
            # 设置当前选中的人格
            if personality_id == current_id:
                card.set_selected(True)
                self.current_personality_id = personality_id
        
        # 更新当前人格信息
        self.update_current_info()
    
    def on_personality_selected(self, personality_id: str):
        """人格选择处理"""
        if personality_id == self.current_personality_id:
            return  # 已经是当前人格，无需切换
        
        # 更新选中状态
        for pid, card in self.personality_cards.items():
            card.set_selected(pid == personality_id)
        
        # 切换人格
        success = self.chat_engine.switch_personality(personality_id)
        if success:
            self.current_personality_id = personality_id
            self.update_current_info()
            self.personality_changed.emit(personality_id)
    
    def update_current_info(self):
        """更新当前人格信息显示"""
        if self.current_personality_id:
            personality = self.chat_engine.personality_manager.get_current_personality()
            if personality:
                info_text = f"{personality['name']}: {personality['description']}"
                traits = personality.get('personality_traits', [])
                if traits:
                    info_text += f"\n特征: {', '.join(traits)}"
                self.current_info_label.setText(info_text)
            else:
                self.current_info_label.setText("人格信息加载失败")
        else:
            self.current_info_label.setText("未选择人格") 