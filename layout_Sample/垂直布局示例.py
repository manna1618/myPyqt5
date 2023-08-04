import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLabel


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 窗体标题和尺寸
        self.setWindowTitle('NB的xx系统')

        # 窗体的尺寸
        self.resize(980, 450)

        # 窗体位置
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

        layout = QVBoxLayout()  # 垂直
        # 头部按钮
        layout.addLayout(self.init_header())
        # 表单区域
        layout.addLayout(self.init_form())
        # 表格区域
        layout.addLayout(self.init_table())
        # 底部按钮
        layout.addLayout(self.init_footer())

        self.setLayout(layout)

    def init_header(self):
        header = QHBoxLayout()
        header.addWidget(QPushButton("开始"))
        header.addWidget(QPushButton("停止"))
        header.addStretch(1)
        return header

    def init_form(self):
        form = QHBoxLayout()
        txt = QLineEdit()
        txt.setPlaceholderText("请输入关键字")
        form.addWidget(txt)
        form.addWidget(QPushButton("添加"))
        return form

    def init_table(self):
        headers = [("ID", 100), ("姓名", 100), ("邮箱", 200), ("标题", 50), ("状态", 50), ("频率", 100)]
        table = QHBoxLayout()
        t = QTableWidget(2, len(headers))
        for idx, ele in enumerate(headers):
            text, width = ele

            item = QTableWidgetItem()
            item.setText(text)
            t.setHorizontalHeaderItem(idx, item)
            t.setColumnWidth(idx, width)

        table.addWidget(t)
        return table

    def init_footer(self):
        footer = QHBoxLayout()
        footer.addWidget(QLabel("待执行"))
        footer.addStretch(1)
        footer.addWidget(QPushButton("初始化"))
        footer.addWidget(QPushButton("重新监测"))
        footer.addWidget(QPushButton("清零"))
        footer.addWidget(QPushButton("邮箱"))
        footer.addWidget(QPushButton("代理"))
        return footer


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
