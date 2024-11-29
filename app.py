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
        self._field_layout = None
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
        start_game_btn.clicked.connect(self.__on_start_game_btn_click)
        layout.addWidget(start_game_btn)
        return layout


    def __init_field(self):
        field_container = QWidget(self)
        layout = QHBoxLayout(field_container)
        label = QLabel("Выберите размер поля и начните игру", parent=field_container)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)
        field_container.setLayout(layout)
        self._field_widget = label
        self._field_layout = layout
        return field_container


    def __replace_field(self, new_field):
        self._field_layout.replaceWidget(self._field_widget, new_field)
        self._field_widget.deleteLater()
        self._field_widget = new_field


    def __draw_field(self, size=3):
        field = QWidget()
        layout = QGridLayout(field)
        for i in range(0, size):
            for j in range(0, size):
                btn = QPushButton(self._field_widget)
                btn.setText(f"{i} {j}")
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                layout.addWidget(btn, i, j)
        return field


    def __on_start_game_btn_click(self):
        self.__replace_field(self.__draw_field(3))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())