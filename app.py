import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QGridLayout,
    QPushButton,
    QWidget,
    QSizePolicy
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__init_ui()


    def __init_ui(self):
        field_layout = self.__init_field()
        center_widget = QWidget(parent=self)
        center_widget.setLayout(field_layout)
        self.setCentralWidget(center_widget)

    
    def __init_field(self):
        layout = QGridLayout()
        for i in range(0, 3):
            for j in range(0, 3):
                btn = QPushButton()
                btn.setText(f"{i} {j}")
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                layout.addWidget(btn, i, j)
        return layout       


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())