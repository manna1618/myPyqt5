import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, \
    QTextEdit
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLabel


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 窗体标题和尺寸
        self.setWindowTitle('NB的xx系统')
        # 窗体的尺寸
        self.resize(1150, 450)
        # 窗体位置
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

        # 创建布局 div
        layout = QHBoxLayout()  # 水平方向
        # (上，下，左，右)边距
        layout.setContentsMargins(10, 10, 10, 10)
        # 左侧布局
        layout.addLayout(self.init_left(), 4)
        # 右侧控件
        layout.addWidget(self.init_right(), 1)

        self.setLayout(layout)

    def init_left(self):
        left = QVBoxLayout()  # 垂直方向
        # 创建表单
        headers = [("ID", 100), ("姓名", 100), ("邮箱", 200), ("标题", 50), ("状态", 50), ("频率", 100)]
        table = QTableWidget(5, len(headers))
        table.setMinimumHeight(400)
        for idx, ele in enumerate(headers):
            text, width = ele
            item = QTableWidgetItem()
            item.setText(text)
            table.setHorizontalHeaderItem(idx, item)
            table.setColumnWidth(idx, width)
        left.addWidget(table)

        footer_layout = QHBoxLayout()  # 水平反向
        lbl = QLabel("待执行")
        footer_layout.addWidget(lbl)
        footer_layout.addStretch(1)
        footer_layout.addWidget(QPushButton("清零"))
        footer_layout.addWidget(QPushButton("邮箱配置"))
        footer_layout.addWidget(QPushButton("IP代理"))
        left.addLayout(footer_layout)

        left.addStretch(1)
        return left

    def init_right(self):
        # 右边
        r = QWidget()
        r.setStyleSheet("border-left:1px solid rgb(245,245,245)")
        right = QVBoxLayout()

        h1 = QHBoxLayout()
        h1.addWidget(QLabel("成功："))
        h1.addWidget(QLabel("100"))
        h1.addStretch(1)
        h1.addWidget(QLabel("失败："))
        h1.addWidget(QLabel("0"))
        right.addLayout(h1)

        h2 = QHBoxLayout()
        h2.addWidget(QLabel("线程："))
        h2.addWidget(QLineEdit("10"))
        h2.addWidget(QPushButton("确定"))
        right.addLayout(h2)

        h3 = QHBoxLayout()
        h3.addWidget(QLabel("卡数："))
        h3.addWidget(QLabel("100"))
        h3.addStretch(1)
        right.addLayout(h3)

        h4 = QHBoxLayout()
        h4.addWidget(QPushButton("加载"))
        h4.addWidget(QPushButton("重置"))
        right.addLayout(h4)

        h5 = QHBoxLayout()
        btn_start = QPushButton("开始")
        btn_start.setFixedHeight(50)
        h5.addWidget(btn_start)
        btn_stop = QPushButton("停止")
        btn_stop.setFixedHeight(50)
        h5.addWidget(btn_stop)
        right.addLayout(h5)

        h6 = QHBoxLayout()
        h6.addWidget(QLabel("运行记录"))
        right.addLayout(h6)

        h7 = QHBoxLayout()
        log = QTextEdit()
        h7.addWidget(log)
        right.addLayout(h7)

        right.addStretch(1)
        r.setLayout(right)
        return r


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
