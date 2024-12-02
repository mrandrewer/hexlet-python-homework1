import sys
import numpy
from functools import partial
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

from field import Field, PlayerType

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._field_layout = None
        self._field_widget = None
        self._field = None
        self._field_buttons = None
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


    def __replace_field(self):
        self._field = Field()
        self._field_buttons = numpy.empty((self._field.field_size, self._field.field_size), dtype=QPushButton)
        new_field_widget = QWidget()
        layout = QGridLayout(new_field_widget)
        for x in range(0, self._field.field_size):
            for y in range(0, self._field.field_size):
                btn = QPushButton(self._field_widget)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                btn.clicked.connect(partial(self.__on_field_btn_click, x, y))
                layout.addWidget(btn, x, y)
                self._field_buttons[x][y] = btn
        self._field_layout.replaceWidget(self._field_widget, new_field_widget)
        self._field_widget.deleteLater()
        self._field_widget = new_field_widget


    def _update_field_btn(self, btn, cell_value):
        if cell_value == PlayerType.PLAYER:
            btn.setText("X")
            btn.setEnabled(False)
        elif cell_value == PlayerType.AI:
            btn.setText("O")
            btn.setEnabled(False)
        else:
            btn.setText("")
            btn.setEnabled(True)


    def _update_field(self):
        for x in range(0, self._field.field_size):
            for y in range(0, self._field.field_size):
                cell_value = self._field.get_cell_value(x, y)
                btn = self._field_buttons[x][y]
                self._update_field_btn(btn, cell_value)


    def __on_start_game_btn_click(self):
        self.__replace_field()

    
    def __on_field_btn_click(self, x, y):
        self._field.make_turn(x, y)
        self._field.make_ai_turn()
        self._update_field()
        print(self._field)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())