__author__ = 'Acko'

import re


class TableState(object):
    """
        Class which represents one Table state.

        It contains information about one (current) table state (move made) in form of
        list (which should not be changed from outside), and also reference to an parent
        TableState instance (necessary for backtracking from solution to beginning).
    """

    TABLE_SIZE = 4
    __EMPTY_BLOCK__ = 'x'

    def __init__(self, state_list, parent):
        """
            Base Constructor, sets all properties to data sent to it.

            :param state_list: (python list|string) list of strings which represents one table state
            :param parent: (TableState *) reference to a parent TableState instance
        """

        self.__state_list = state_list if isinstance(state_list, list) else self.__parse_string(state_list)
        self.parent = parent

    def __str__(self):
        """ Overrides __str__ method from object """

        ret_val = ''
        for i in xrange(self.TABLE_SIZE):
            for j in xrange(self.TABLE_SIZE):
                ret_val += self.__state_list[i * self.TABLE_SIZE + j] + ' '
            ret_val += '\n'
        return ret_val

    def __hash__(self):
        """ Overrides __hash__ method from object """

        return hash(str(self))

    def __eq__(self, other):
        """ Overriding operator==() """

        return self.__state_list == other.__state_list

    def generate_next_moves(self):
        """
            Function which generates next moves based on current table state.

            Based on rules of 15-puzzle game, it simulates all moves which can be make
            from given state. For each new move which can be made it creates new instance of
            TableState and stores it in list which is then returned.

            :return: (python list) list of TableState instances (all possible next moves)
        """

        i = self.__state_list.index(self.__EMPTY_BLOCK__)
        moves = []

        # move left
        if i > 0 and i % self.TABLE_SIZE != 0:
            new_list = list(self.__state_list)
            new_list[i], new_list[i - 1] = new_list[i - 1], new_list[i]
            moves.append(TableState(new_list, self))

        # move up
        if i > self.TABLE_SIZE:
            new_list = list(self.__state_list)
            new_list[i], new_list[i - self.TABLE_SIZE] = new_list[i - self.TABLE_SIZE], new_list[i]
            moves.append(TableState(new_list, self))

        # move right
        if i < len(self.__state_list) - 1 and i % self.TABLE_SIZE != self.TABLE_SIZE - 1:
            new_list = list(self.__state_list)
            new_list[i], new_list[i + 1] = new_list[i + 1], new_list[i]
            moves.append(TableState(new_list, self))

        # move down
        if i < len(self.__state_list) - 1 - self.TABLE_SIZE:
            new_list = list(self.__state_list)
            new_list[i], new_list[i + self.TABLE_SIZE] = new_list[i + self.TABLE_SIZE], new_list[i]
            moves.append(TableState(new_list, self))

        return moves

    def is_final(self):
        """
            Function which checks if current state is final state (puzzle is solved)

            :return: (boolean) True if this TableState is final state, False otherwise
        """

        for index, el in enumerate(self.__state_list):
            if el == self.__EMPTY_BLOCK__:
                return index == len(self.__state_list) - 1
            elif int(el) - 1 != index:
                return False
        return True

    def is_solvable(self):
        """
            Method which determines if given state is solvable or not.

            It uses following rules:
                a) If the grid width is odd, then the number of inversions in a solvable situation is even.
                b) If the grid width is even, and the blank is on an even row counting from the bottom
                    (second-last, fourth-last etc), then the number of inversions in a solvable situation is odd.
                c) If the grid width is even, and the blank is on an odd row counting from the bottom
                    (last, third-last, fifth-last etc) then the number of inversions in a solvable situation is even.

            or "mathematically":
                ( (grid width odd) && (#inversions even) )  ||
                ( (grid width even) && ((blank on odd row from bottom) == (#inversions even)) )
        """

        inversions = self.__calculate_inversions()
        empty_tile_row = self.__state_list.index(self.__EMPTY_BLOCK__) // self.TABLE_SIZE

        return (self.TABLE_SIZE % 2 == 1 and inversions % 2 == 1) or\
            (self.TABLE_SIZE % 2 == 0 and (self.TABLE_SIZE - 1 - empty_tile_row) % 2 == inversions % 2)

    def __calculate_inversions(self):
        """
            Helper method which calculates number of inversions for a given puzzle state.

            :return: (int) number of inversions in current puzzle state
        """
        inversions = 0
        for i in xrange(len(self.__state_list) - 1):
            if self.__state_list[i] == self.__EMPTY_BLOCK__:
                continue

            for j in xrange(i + 1, len(self.__state_list)):
                if self.__state_list[j] != self.__EMPTY_BLOCK__ and int(self.__state_list[j]) < int(self.__state_list[i]):
                    inversions += 1
        return inversions

    def manhattan(self):
        """
            Function that calculates "manhattan" distance for current TableState.

            This function calculates "manhattan" distance for current state, and it can be used
            as heuristics function when sorting all table states.

            :return: (int) "Manhattan" distance for current state
        """

        manhattan_distance = 0
        for i in xrange(len(self.__state_list)):
            if self.__state_list[i] == self.__EMPTY_BLOCK__:
                continue

            x1, y1 = i // self.TABLE_SIZE, i % self.TABLE_SIZE
            x2, y2 = (int(self.__state_list[i]) - 1) // self.TABLE_SIZE, (int(self.__state_list[i]) - 1) % self.TABLE_SIZE

            manhattan_distance += abs(x2 - x1) + abs(y2 - y1)

        return manhattan_distance

    def hamming(self):
        """
            Function which returns number of tiles which are not in the "right" place.

            This function calculates number of tiles which are not placed right, and returns that number,
            it can be used as heuristics function when sorting all table states.

            :return: (int) number of tiles which are not in the "right" place
        """

        hamming = 0
        for i in xrange(len(self.__state_list)):
            if self.__state_list[i] == self.__EMPTY_BLOCK__:
                continue

            if int(self.__state_list[i]) - 1 != i:
                hamming += 1

        return hamming

    def __parse_string(self, string_):
        """ Helper method which goes parses string finding all number inputs and __EMPTY_BLOCK__ string literal """

        if not isinstance(string_, str):
            raise Exception('Invalid data')
        return re.findall(r'\d+|' + self.__EMPTY_BLOCK__, string_)