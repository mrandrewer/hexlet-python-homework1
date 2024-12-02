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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._field_layout = None
        self._field_widget = None
        self._field_data = None
        self._field_buttons = None
        self._field_size = 3
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
        self._field_data = numpy.zeros((self._field_size, self._field_size), dtype=int)
        self._field_buttons = numpy.empty((self._field_size, self._field_size), dtype=QPushButton)
        new_field = QWidget()
        layout = QGridLayout(new_field)
        for x in range(0, self._field_size):
            for y in range(0, self._field_size):
                btn = QPushButton(self._field_widget)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                btn.clicked.connect(partial(self.__on_field_btn_click, x, y))
                layout.addWidget(btn, x, y)
                self._field_buttons[x][y] = btn
        self._field_layout.replaceWidget(self._field_widget, new_field)
        self._field_widget.deleteLater()
        self._field_widget = new_field


    def _ckeck_win_condition(self):


    def _make_turn(self, x, y, player=True):
        self._field_data[x][y] = 1 if player else -1
        self._field_buttons[x][y].setText(f"x" if player else "o")
        self._field_buttons[x][y].setEnabled(False)
        print(self._field_data)


    def _make_ai_turn(self):
        (x, y) = self._select_ai_position()
        self._make_turn(x, y, player=False)


    def _select_ai_position(self):
        for x in range(0, self._field_size):
            for y in range(0, self._field_size):
                if self._field_data[x][y] == 0:
                    return (x, y)
        return None


    def __on_start_game_btn_click(self):
        self.__replace_field()

    
    def __on_field_btn_click(self, x, y):
       self._make_turn(x, y)
       self._make_ai_turn()

    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())