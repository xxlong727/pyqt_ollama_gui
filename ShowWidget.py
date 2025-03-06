from PyQt5.QtWidgets import QTextEdit

class ShowWidget:
    """中间文本显示类"""
    def __init__(self, parent):
        self.parent = parent
        
    def init_layout(self):
        text_area = QTextEdit()
        text_area.setReadOnly(True) 
        text_area.setFontPointSize(15)
        
        self.parent.text_area = text_area
        self.parent.content = None
        
        return text_area