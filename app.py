import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QSizePolicy
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._field_size_spin = None
        self._field_widget = None
        self.__init_ui()


    def __init_ui(self):
        layout = QVBoxLayout()
        layout.addLayout(self.__init_settings())
        layout.addWidget(self.__init_field())
        center_widget = QWidget(parent=self)
        center_widget.setLayout(layout)
        self.setCentralWidget(center_widget)
    

    def __init_settings(self):
        layout = QHBoxLayout()
        label = QLabel("Размер поля: ", parent=self)
        layout.addWidget(label)
        self._field_size_spin = QSpinBox(self) 
        layout.addWidget(self._field_size_spin)
        start_game_btn = QPushButton("Начать игру")
        layout.addWidget(start_game_btn)
        return layout


    def __init_field(self):
        self._field_widget = QWidget(self)
        layout = QHBoxLayout(self._field_widget)
        label = QLabel("Выберите размер поля и начните игру", parent=self._field_widget)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)
        self._field_widget.setLayout(layout)
        return self._field_widget


    def __draw_field(self):
        for child in list(self._field_widget.children()):
            child.deleteLater()

        layout = QGridLayout()
        for i in range(0, 3):
            for j in range(0, 3):
                btn = QPushButton(self._field_widget)
                btn.setText(f"{i} {j}")
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                layout.addWidget(btn, i, j)
        self._field_widget.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())