# -*- coding: utf-8 -*-
"""
人格选择界面组件
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QButtonGroup, QRadioButton,
                             QTextEdit, QFrame, QScrollArea, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QFont, QPalette, QColor


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
        self.setFixedHeight(140)  # 增加高度给更多空间
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)  # 增加边距
        layout.setSpacing(12)
        
        # 顶部区域：人格名称和装饰点
        top_layout = QHBoxLayout()
        
        # 人格名称
        self.name_label = QLabel(self.personality_data.get('name', self.personality_id))
        name_font = QFont()
        name_font.setPointSize(14)
        name_font.setBold(True)
        self.name_label.setFont(name_font)
        top_layout.addWidget(self.name_label)
        
        top_layout.addStretch()
        
        # 装饰点（显示人格类型）
        self.type_dot = QLabel("●")
        type_font = QFont()
        type_font.setPointSize(16)
        self.type_dot.setFont(type_font)
        top_layout.addWidget(self.type_dot)
        
        layout.addLayout(top_layout)
        
        # 人格描述
        self.desc_label = QLabel(self.personality_data.get('description', ''))
        self.desc_label.setWordWrap(True)
        desc_font = QFont()
        desc_font.setPointSize(11)
        self.desc_label.setFont(desc_font)
        layout.addWidget(self.desc_label)
        
        # 特征标签区域
        traits = self.personality_data.get('personality_traits', [])
        if traits:
            traits_layout = QHBoxLayout()
            traits_layout.setSpacing(6)
            
            # 只显示前3个特征，避免拥挤
            for i, trait in enumerate(traits[:3]):
                trait_label = QLabel(trait)
                trait_font = QFont()
                trait_font.setPointSize(9)
                trait_label.setFont(trait_font)
                trait_label.setAlignment(Qt.AlignCenter)
                traits_layout.addWidget(trait_label)
                
                # 保存特征标签的引用，用于样式设置
                if not hasattr(self, 'trait_labels'):
                    self.trait_labels = []
                self.trait_labels.append(trait_label)
            
            traits_layout.addStretch()
            layout.addLayout(traits_layout)
        else:
            self.trait_labels = []
    
    def get_personality_color(self):
        """根据人格ID获取专属颜色"""
        colors = {
            "friendly": "#4CAF50",      # 绿色 - 友善
            "humorous": "#FF9800",      # 橙色 - 幽默
            "knowledgeable": "#2196F3", # 蓝色 - 知识
            "creative": "#9C27B0",      # 紫色 - 创意
            "calm": "#607D8B"           # 蓝灰色 - 沉稳
        }
        return colors.get(self.personality_id, "#007acc")
    
    def set_style(self):
        """设置样式"""
        self.set_selected(self.is_selected)
        self.update_all_colors()
    
    def update_all_colors(self):
        """更新所有元素的颜色"""
        personality_color = self.get_personality_color()
        
        if self.is_dark_theme:
            name_color = "#ffffff"
            desc_color = "#cccccc"
            trait_bg = "#404040"
            trait_text = "#e0e0e0"
        else:
            name_color = "#2c3e50"
            desc_color = "#5a6c7d"
            trait_bg = "#f8f9fa"
            trait_text = "#6c757d"
        
        # 设置名称颜色
        self.name_label.setStyleSheet(f"color: {name_color}; background: transparent; border: none;")
        
        # 设置描述颜色
        self.desc_label.setStyleSheet(f"""
            color: {desc_color}; 
            background: transparent; 
            border: none;
            line-height: 1.4;
        """)
        
        # 设置装饰点颜色
        self.type_dot.setStyleSheet(f"color: {personality_color}; background: transparent; border: none;")
        
        # 设置特征标签样式
        for trait_label in self.trait_labels:
            trait_label.setStyleSheet(f"""
                background-color: {trait_bg};
                color: {trait_text};
                border: 1px solid {personality_color}40;
                border-radius: 10px;
                padding: 3px 8px;
                margin: 1px;
            """)
    
    def set_selected(self, selected: bool):
        """设置选中状态"""
        self.is_selected = selected
        personality_color = self.get_personality_color()
        
        if self.is_dark_theme:
            if selected:
                bg_color = "#2a2a2a"
                border_color = personality_color
                border_width = "2px"
                shadow = f"0px 6px 20px rgba(0, 0, 0, 0.6), 0px 0px 15px {personality_color}60"
            else:
                bg_color = "#363636"
                border_color = "#555555"
                border_width = "1px"
                shadow = "0px 2px 8px rgba(0, 0, 0, 0.4)"
        else:
            if selected:
                bg_color = "#ffffff"
                border_color = personality_color
                border_width = "2px"
                shadow = f"0px 6px 20px rgba(0, 0, 0, 0.15), 0px 0px 15px {personality_color}40"
            else:
                bg_color = "#ffffff"
                border_color = "#e1e8ed"
                border_width = "1px"
                shadow = "0px 2px 8px rgba(0, 0, 0, 0.1)"
        
        # 悬浮时的样式
        if self.is_dark_theme:
            hover_shadow = f"0px 8px 25px rgba(0, 0, 0, 0.7), 0px 0px 20px {personality_color}80"
        else:
            hover_shadow = f"0px 8px 25px rgba(0, 0, 0, 0.2), 0px 0px 20px {personality_color}60"
        
        style = f"""
        PersonalityCard {{
            background-color: {bg_color};
            border: {border_width} solid {border_color};
            border-radius: 16px;
            margin: 3px;
            box-shadow: {shadow};
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        PersonalityCard:hover {{
            border-color: {personality_color};
            box-shadow: {hover_shadow};
            transform: translateY(-3px);
        }}
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