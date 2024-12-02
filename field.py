from copy import deepcopy
from enum import IntEnum
import numpy

class PlayerType(IntEnum):
    AI = -1
    NOBODY = 0
    PLAYER = 1

class Field:

    def __init__(self):
        self.field_size = 3
        self.field_data = numpy.zeros((self.field_size, self.field_size), dtype=int)


    def _get_winner(self, field_data):
        for i in range(0, self.field_size):
            if field_data[i][0] != 0 and field_data[i][0] == field_data[i][1] == field_data[i][2]:
                return PlayerType(field_data[i][0])
            if field_data[0][i] != 0 and field_data[0][i] == field_data[1][i] == field_data[2][i]:
                return PlayerType(field_data[0][i])
        if field_data[0][0] != 0 and field_data[0][0] == field_data[1][1] == field_data[2][2]:
            return PlayerType(field_data[0][0])
        if field_data[0][2] != 0 and field_data[0][2] == field_data[1][1] == field_data[2][0]:
            return PlayerType(field_data[0][2])
        return PlayerType(0)


    def _game_over(self, field_data):
        if self.has_winner(field_data):
            return True
        for x in range(0, self.field_size):
            for y in range(0, self.field_size):
                if PlayerType(field_data[x][y]) == PlayerType.NOBODY:
                    return False
        return True


    def _get_allowed_moves(self, field_data):
        allowed_actions = []
        for x in range(0, self.field_size):
            for y in range(0, self.field_size):
                if PlayerType(field_data[x][y]) == PlayerType.NOBODY:
                    allowed_actions.append((x, y))
        return allowed_actions
    

    def _apply_move(self, field_data, x, y, playerType):
        result = deepcopy(field_data)
        result[x][y] = int(playerType)
        return result


    def _rate_field_max(self, field_data):
        rate = float('-inf')
        winner = self._get_winner(field_data)
        if winner != PlayerType.NOBODY:
            return winner
        for action in self._get_allowed_moves(field_data):
            (x, y) = action
            rate = max(
                rate,
                self._rate_field_min(
                    self._apply_move(field_data, x, y, PlayerType.PLAYER)))
        return rate

    
    def _rate_field_min(self, field_data):
        rate = float('inf')
        winner = self._get_winner(field_data)
        if winner != PlayerType.NOBODY:
            return winner
        for action in self._get_allowed_moves(field_data):
            (x, y) = action
            rate = min(
                rate,
                self._rate_field_max(
                    self._apply_move(field_data, x, y, PlayerType.AI)))
        return rate
    

    def make_ai_turn(self):
        allowed_actions = self._get_allowed_moves(self.field_data)
        print(allowed_actions)
        move_results = []
        for action in allowed_actions:
            (x, y) = action
            move_results.append([
                self._rate_field_min(self._apply_move(self.field_data, x, y, PlayerType.AI)),
                action])
        ai_action = sorted(move_results, key=lambda r: r[0], reverse=True)[0][1]
        (x, y) = ai_action
        self.make_turn(x, y, player=False)


    def make_turn(self, x, y, player=True):
        self.field_data[x][y] = 1 if player else -1

    
    def get_cell_value(self, x, y):
        return PlayerType(self.field_data[x][y])


    def get_winner(self):
        return self._get_winner(self.field_data)


    def __str__(self):
        return str(self.field_data)