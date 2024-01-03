import sys
import time
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QDialog
from PySide6.QtGui import QMovie


# 创建一个QThread类用于执行耗时任务
class LongTaskThread(QThread):
    finished = Signal()

    def run(self):
        # 模拟耗时任务
        time.sleep(5)
        self.finished.emit()


# 创建一个封装了加载动画的QDialog类
class LoadingAnimationDialog(QDialog):
    def __init__(self, gif_path, parent=None):
        super().__init__(parent, Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setModal(True)  # 设置为模态窗口
        self.init_ui(gif_path)

    def init_ui(self, gif_path):
        self.loading_label = QLabel()
        self.loading_movie = QMovie(gif_path)
        self.loading_label.setMovie(self.loading_movie)

        layout = QVBoxLayout()
        layout.addWidget(self.loading_label)
        self.setLayout(layout)
        self.loading_movie.start()


# 创建一个类用于管理加载动画的显示和隐藏
class LoadingAnimation:
    def __init__(self, gif_path, parent=None):
        self.dialog = LoadingAnimationDialog(gif_path, parent)

    def show(self):
        self.dialog.show()

    def hide(self):
        self.dialog.accept()


# 创建一个主窗口类，其中包含了启动和完成任务的逻辑
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Long Task with Loading Animation")
        self.long_task_thread = LongTaskThread()
        self.long_task_thread.finished.connect(self.on_finished)
        self.loading_animation = None  # 引用加载动画
        self.init_ui()

    def init_ui(self):
        self.start_button = QPushButton("Start Long Task")
        self.start_button.clicked.connect(self.start_long_task)

        layout = QVBoxLayout()
        layout.addWidget(self.start_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_long_task(self):
        self.start_button.setEnabled(False)
        if not self.loading_animation:
            self.loading_animation = LoadingAnimation("gif/gzz.gif", self)
        self.loading_animation.show()
        self.long_task_thread.start()

    def on_finished(self):
        if self.loading_animation:
            self.loading_animation.hide()
        self.start_button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
