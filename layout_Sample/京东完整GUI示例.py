import json
import os
import sys
import time

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLabel, QMessageBox

DB_FOLDER_PATH = os.path.join("db")
DB_FILE_PATH = os.path.join("db", "db.json")


class STATUS:
    init = "初始化中"
    ready = "等执行"
    init_fail = "初始化失败"
    processing = "监测中"
    success = "完成并提醒"
    error = "执行异常"


class SWITCH:
    stop = 1
    stopping = 2
    running = 3


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 默认是停止中
        self.switch = SWITCH.stop

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

        btn_start = QPushButton("开始")
        btn_start.clicked.connect(self.event_click_start)
        header.addWidget(btn_start)

        btn_stop = QPushButton("停止")
        btn_stop.clicked.connect(self.event_click_stop)

        header.addWidget(btn_stop)
        header.addStretch(1)
        return header
    def event_click_stop(self):

        # 1.状态问题，一定要是正在执行中
        if self.switch != SWITCH.running:
            QMessageBox.warning(self, "错误", "未运行请勿点击停止")
            return

        # 2.状态更新为 停止中
        self.switch = SWITCH.stopping

        # 3.
        # 要执行的XXX代码
    def init_form(self):
        form = QHBoxLayout()

        self.txt = txt = QLineEdit()
        # txt.setText("100005907830=1000")
        txt.setPlaceholderText("请输入信息，格式为：商品ID=目标价格；示例：100005907830=1000")

        form.addWidget(txt)

        btn_add = QPushButton("添加")
        btn_add.clicked.connect(self.event_click_add)
        form.addWidget(btn_add)
        return form

    def event_click_add(self):
        # 1.获取数据框中的内容
        text = self.txt.text().strip()
        if not text:
            QMessageBox.warning(self, "错误", "请输入商品ID和价格")
            return

        # 2.格式处理 sdfsdf=213
        sku_id, price = text.split("=")

        # 3.构造商品列表
        url = "https://item.jd.com/{}.html".format(sku_id)
        new_row_list = [sku_id, "", url, price, STATUS.init]

        # 4.加入表格
        # headers = [("商品ID", 100), ("标题", 300), ("URL", 250), ("价格", 100), ("状态", 100)]
        # 4.1 找到表格  self.table_widget
        # 4.2 表格添加一行
        current_row_count = self.table_widget.rowCount()
        self.table_widget.insertRow(current_row_count)

        # 4.3 写入添加的表格
        for col, text in enumerate(new_row_list):
            cell = QTableWidgetItem(text)
            self.table_widget.setItem(current_row_count, col, cell)

        # 5.根据商品ID获取商品详细 & 获取结果更新会表格
        #      新建线程             告知窗体更新表格
        from utils.threads import NewTaskThread
        thread = NewTaskThread(sku_id, current_row_count, self)
        thread.success.connect(self.init_task_success_callback)
        thread.error.connect(self.init_task_error_callback)
        thread.start()

    def init_task_success_callback(self, row_index, text):
        print("初始化成功：", row_index, text)
        # 1.表格的更新：标题、状态
        self.table_widget.setItem(row_index, 1, QTableWidgetItem(text))
        self.table_widget.setItem(row_index, 4, QTableWidgetItem(STATUS.ready))

        # 2.获取当前行数据
        row_text = []
        for i in range(5):
            text = self.table_widget.item(row_index, i).text()
            row_text.append(text)

        # 3.持久化存储：txt、json格式、SQLite、access
        old_list = self.db_get_old_list()
        old_list.append(row_text)
        self.db_save_list(old_list)

    def init_task_error_callback(self, row_index, text):
        print("初始化失败：", row_index, text)
        # 1.表格的更新：标题、状态
        self.table_widget.setItem(row_index, 1, QTableWidgetItem(text))
        self.table_widget.setItem(row_index, 4, QTableWidgetItem(STATUS.init_fail))

        # 2.获取当前行数据
        row_text = []
        for i in range(5):
            text = self.table_widget.item(row_index, i).text()
            row_text.append(text)

        # 3.持久化存储：txt、json格式、SQLite、access
        old_list = self.db_get_old_list()
        old_list.append(row_text)
        self.db_save_list(old_list)

    def db_get_old_list(self):
        if not os.path.exists(DB_FILE_PATH):
            old_list = []
        else:
            with open(DB_FILE_PATH, mode='r', encoding='utf-8') as f:
                old_list = json.load(f)
        return old_list

    def db_save_list(self, data_list):
        if not os.path.exists(DB_FOLDER_PATH):
            os.makedirs(DB_FOLDER_PATH)

        with open(DB_FILE_PATH, mode='w', encoding='utf-8') as f:
            json.dump(data_list, f, ensure_ascii=False)

    def init_table(self):
        # headers = [("ID", 100), ("姓名", 100), ("邮箱", 200), ("标题", 50), ("状态", 50), ("频率", 100)]
        headers = [("商品ID", 100), ("标题", 300), ("URL", 250), ("价格", 100), ("状态", 100)]
        table = QHBoxLayout()
        # 创建表格
        self.table_widget = t = QTableWidget(0, len(headers))

        # 设置表头
        for idx, ele in enumerate(headers):
            text, width = ele

            item = QTableWidgetItem()
            item.setText(text)
            t.setHorizontalHeaderItem(idx, item)
            t.setColumnWidth(idx, width)

        # 加载默认数据
        current_row_count = t.rowCount()
        old_list = self.db_get_old_list()
        for row_list in old_list:
            t.insertRow(current_row_count)
            for i in range(5):
                t.setItem(current_row_count, i, QTableWidgetItem(row_list[i]))
            current_row_count += 1

        # 开启右键功能
        t.setContextMenuPolicy(Qt.CustomContextMenu)
        t.customContextMenuRequested.connect(self.table_right_menu)

        table.addWidget(t)
        return table

    def table_right_menu(self, pos):
        # 1.支持选中1行才能右键
        selected_item_list = self.table_widget.selectedItems()
        if len(selected_item_list) != 1:
            return

        # 2.显示菜单
        from PyQt5.QtWidgets import QMenu
        menu = QMenu()
        item_copy = menu.addAction("复制")
        item_log = menu.addAction("查看日志")
        item_log_clear = menu.addAction("清除日志")

        # 2.用户选择了那个菜单？
        action = menu.exec_(self.table_widget.mapToGlobal(pos))

        if action == item_copy:
            clipboard = QApplication.clipboard()
            clipboard.setText(selected_item_list[0].text())

        if action == item_log_clear:
            row_index = selected_item_list[0].row()
            sku_id = self.table_widget.item(row_index, 0).text().strip()
            file_path = os.path.join("log", "{}.log".format(sku_id))
            if os.path.exists(file_path):
                os.remove(file_path)

        if action == item_log:
            # 打开对话框，在对话框中显示日志详细
            row_index = selected_item_list[0].row()
            sku_id = self.table_widget.item(row_index, 0).text().strip()
            from utils.dialog import LogDialog

            dialog = LogDialog(sku_id)
            dialog.setWindowModality(Qt.ApplicationModal)
            dialog.exec_()

    def init_footer(self):
        footer = QHBoxLayout()
        self.lbl_status = lbl_status = QLabel("待执行")
        footer.addWidget(lbl_status)
        footer.addStretch(1)

        btn_repeat_init = QPushButton("重新初始化")
        btn_repeat_init.clicked.connect(self.event_click_repeat_init)
        footer.addWidget(btn_repeat_init)

        btn_delete = QPushButton("删除")
        btn_delete.clicked.connect(self.event_click_delete)
        footer.addWidget(btn_delete)

        btn_email = QPushButton("邮箱")
        btn_email.clicked.connect(self.event_click_email)
        footer.addWidget(btn_email)

        footer.addWidget(QPushButton("代理"))
        return footer

    def event_click_delete(self):
        print("点击删除")
        # 1.获取已选中的行
        row_list = self.table_widget.selectionModel().selectedRows()
        if not row_list:
            return

        # 2.表格中删除
        idx_list = []  # [2,1]
        row_list.reverse()
        for row_object in row_list:
            index = row_object.row()
            self.table_widget.setItem(index, 4, QTableWidgetItem(STATUS.init))
            idx_list.append(index)
            self.table_widget.removeRow(index)

        # 3.文件中删除
        old_list = self.db_get_old_list()
        for idx in idx_list:
            del old_list[idx]
        self.db_save_list(old_list)

    def event_click_repeat_init(self):
        print("重新初始化")

        # 1.获取已选中的行
        row_list = self.table_widget.selectionModel().selectedRows()
        if not row_list:
            return

        # 2.循环所有行  sku_id、索引、状态：初始化中 -> 更新状态
        for row_object in row_list:
            row_idx = row_object.row()
            sku_id = self.table_widget.item(row_idx, 0).text().strip()
            self.table_widget.setItem(row_idx, 4, QTableWidgetItem(STATUS.init))

            from utils.threads import NewTaskThread
            thread = NewTaskThread(sku_id, row_idx, self)
            thread.success.connect(self.repeat_init_task_success_callback)
            thread.error.connect(self.repeat_init_task_error_callback)
            thread.start()

    def repeat_init_task_success_callback(self, row_index, text):
        print("初始化成功：", row_index, text)
        # 1.表格的更新：标题、状态
        self.table_widget.setItem(row_index, 1, QTableWidgetItem(text))
        self.table_widget.setItem(row_index, 4, QTableWidgetItem(STATUS.ready))

        # 2.获取当前行数据
        row_text = []
        for i in range(5):
            ele = self.table_widget.item(row_index, i).text()
            row_text.append(ele)

        # 3.持久化存储：txt、json格式、SQLite、access
        old_list = self.db_get_old_list()
        old_list[row_index][1] = text
        old_list[row_index][4] = STATUS.ready

        self.db_save_list(old_list)

    def repeat_init_task_error_callback(self, row_index, text):
        print("初始化失败：", row_index, text)
        # 1.表格的更新：标题、状态
        self.table_widget.setItem(row_index, 1, QTableWidgetItem(text))
        self.table_widget.setItem(row_index, 4, QTableWidgetItem(STATUS.init_fail))

        # 2.获取当前行数据
        row_text = []
        for i in range(5):
            ele = self.table_widget.item(row_index, i).text()
            row_text.append(ele)

        # 3.持久化存储：txt、json格式、SQLite、access
        old_list = self.db_get_old_list()
        old_list[row_index][1] = text
        old_list[row_index][4] = STATUS.init_fail
        self.db_save_list(old_list)

    def event_click_email(self):
        # 再打开一个新的窗体
        from utils.dialog import EmailDialog

        dialog = EmailDialog()
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

    def event_click_start(self):
        """ 点击开始 """

        # 1.重复点击开始的问题
        if self.switch != SWITCH.stop:
            QMessageBox.warning(self, '错误', "正在执行，请勿重复操作")
            return

        # 2.状态更新为
        self.switch = SWITCH.running

        # 3.读取表格中的监控项，为每个监控项创建一个线程，线程维护在一个列表中
        from utils.scheduler import SCHEDULER
        SCHEDULER.start(self, self.task_success_callback, self.task_error_callback, self.task_stop_callback)

        # 4.状态标志更新
        self.update_status_message("执行中")

    def task_success_callback(self, row_index):
        print("任务执行完成")
        # 1.表格状态更新
        cell_status = QTableWidgetItem(STATUS.success)
        self.table_widget.setItem(row_index, 4, cell_status)

        # 2.文件更新
        old_list = self.db_get_old_list()
        old_list[row_index][4] = STATUS.success
        self.db_save_list(old_list)
        print("任务执行完成 信息:", old_list)
        from utils import send_email
        for item in old_list:
            if item[-1] == '完成并提醒':
                info = ','.join(item)
                print(info)
                send_email.Email(info)


    def task_error_callback(self, row_index, text):
        print("任务执行失败")
        # 1.表格状态更新
        cell_status = QTableWidgetItem(STATUS.error)
        self.table_widget.setItem(row_index, 4, cell_status)

        # 2.文件更新
        old_list = self.db_get_old_list()
        old_list[row_index][4] = STATUS.error
        self.db_save_list(old_list)

    def task_stop_callback(self, row_index):
        print("任务停止")
        # 1.表格状态更新
        cell_status = QTableWidgetItem(STATUS.ready)
        self.table_widget.setItem(row_index, 4, cell_status)

    def event_click_stop(self):

        # 1.状态问题，一定要是正在执行中
        if self.switch != SWITCH.running:
            QMessageBox.warning(self, "错误", "未运行请勿点击停止")
            return

        # 2.状态更新为 停止中
        self.switch = SWITCH.stopping

        # 3.让正在执行的线程停下来 & 准实时更新（1s）
        from utils.scheduler import SCHEDULER
        SCHEDULER.stop(self, self.update_status_message)

    def update_status_message(self, txt):
        # 已停止  停止中（10）
        if txt == "已终止":
            self.switch = SWITCH.stop
        self.lbl_status.setText(txt)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
