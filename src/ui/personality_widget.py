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
    
    def __init__(self, personality_id: str, personality_data: dict):
        super().__init__()
        self.personality_id = personality_id
        self.personality_data = personality_data
        self.is_selected = False
        
        self.init_ui()
        self.set_style()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)
        
        # 人格名称
        name_label = QLabel(self.personality_data.get('name', self.personality_id))
        # 使用系统兼容的字体
        try:
            from utils.helpers import get_system_font
            name_font = get_system_font(12, bold=True)
            if name_font:
                name_label.setFont(name_font)
        except ImportError:
            # 如果导入失败，使用默认字体
            name_font = QFont()
            name_font.setPointSize(12)
            name_font.setBold(True)
            name_label.setFont(name_font)
        layout.addWidget(name_label)
        
        # 人格描述
        desc_label = QLabel(self.personality_data.get('description', ''))
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(desc_label)
        
        # 人格特征
        traits = self.personality_data.get('personality_traits', [])
        if traits:
            traits_text = "特征: " + ", ".join(traits)
            traits_label = QLabel(traits_text)
            traits_label.setWordWrap(True)
            traits_label.setStyleSheet("color: #888; font-size: 10px; font-style: italic;")
            layout.addWidget(traits_label)
        
        # 设置固定高度
        self.setFixedHeight(120)
    
    def set_style(self):
        """设置样式"""
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
    
    def set_selected(self, selected: bool):
        """设置选中状态"""
        self.is_selected = selected
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
        
        self.init_ui()
        self.load_personalities()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # 标题
        title_label = QLabel("选择AI人格")
        try:
            from utils.helpers import get_system_font
            title_font = get_system_font(14, bold=True)
            if title_font:
                title_label.setFont(title_font)
        except ImportError:
            title_font = QFont()
            title_font.setPointSize(14)
            title_font.setBold(True)
            title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 说明文字
        desc_label = QLabel("不同的人格会展现不同的对话风格和记忆关注点")
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("color: #666; font-size: 11px; margin-bottom: 10px;")
        layout.addWidget(desc_label)
        
        # 滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # 人格卡片容器
        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(10)
        self.cards_layout.addStretch()  # 添加弹性空间
        
        scroll_area.setWidget(self.cards_container)
        layout.addWidget(scroll_area)
        
        # 当前人格信息显示
        self.create_current_info_panel()
        layout.addWidget(self.current_info_frame)
    
    def create_current_info_panel(self):
        """创建当前人格信息面板"""
        self.current_info_frame = QFrame()
        self.current_info_frame.setFixedHeight(100)
        
        layout = QVBoxLayout(self.current_info_frame)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 标题
        info_title = QLabel("当前人格")
        try:
            from utils.helpers import get_system_font
            info_font = get_system_font(11, bold=True)
            if info_font:
                info_title.setFont(info_font)
        except ImportError:
            info_font = QFont()
            info_font.setPointSize(11)
            info_font.setBold(True)
            info_title.setFont(info_font)
        layout.addWidget(info_title)
        
        # 当前人格信息
        self.current_info_label = QLabel("未选择人格")
        self.current_info_label.setWordWrap(True)
        self.current_info_label.setStyleSheet("color: #666; font-size: 10px;")
        layout.addWidget(self.current_info_label)
        
        # 设置样式
        self.current_info_frame.setStyleSheet("""
        QFrame {
            background-color: #f8f9fa;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
        }
        """)
    
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
            card = PersonalityCard(personality_id, personality_data)
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