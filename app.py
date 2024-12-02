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
    QPushButton,
    QSizePolicy,
    QMessageBox
)

from field import Field, PlayerType

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._field = None
        self._field_buttons = None
        self.__create_field()
        self.__init_ui()


    def __create_field(self):
        self._field = Field()


    def __init_ui(self):
        self.setWindowTitle("Крестики нолики")
        layout = QVBoxLayout()
        layout.addLayout(self.__init_settings())
        layout.addWidget(self.__init_field())
        center_widget = QWidget(parent=self)
        center_widget.setLayout(layout)
        self.setCentralWidget(center_widget)
    

    def __init_settings(self):
        layout = QHBoxLayout()
        start_game_btn = QPushButton("Начать игру заново")
        start_game_btn.clicked.connect(self.__on_start_game_btn_click)
        layout.addWidget(start_game_btn)
        return layout


    def __init_field(self):
        self._field_buttons = numpy.empty((self._field.field_size, self._field.field_size), dtype=QPushButton)
        field_container = QWidget(self)
        layout = QGridLayout(field_container)
        for x in range(0, self._field.field_size):
            for y in range(0, self._field.field_size):
                btn = QPushButton(field_container)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                btn.clicked.connect(partial(self.__on_field_btn_click, x, y))
                layout.addWidget(btn, x, y)
                self._field_buttons[x][y] = btn
        field_container.setLayout(layout)
        return field_container


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


    def start_game(self):
        self.__create_field()
        self._update_field()

    def finish_game(self, winner):
        self._update_field()
        msg = QMessageBox() 
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"Игра закончена! Победил {'игрок' if winner == PlayerType.PLAYER else 'компьютер'}") 
        msg.setWindowTitle("Игра закончена")  
        msg.setStandardButtons(QMessageBox.Ok) 
        msg.exec_()
        self.start_game()

    
    def check_winner(self):
        winner = self._field.get_winner()
        if winner != PlayerType(0):
            self.finish_game(winner)
            return True
        return False


    def __on_start_game_btn_click(self):
       self.start_game()

    
    def __on_field_btn_click(self, x, y):
        self._field.make_turn(x, y)
        if self.check_winner():
            return
        self._field.make_ai_turn()
        if self.check_winner():
            return
        self._update_field()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())