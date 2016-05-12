__author__ = 'Acko'

from datetime import datetime

from application.TableState import TableState
from application.functions import solve_puzzle, print_results


if __name__ == '__main__':
    TableState.TABLE_SIZE = 4
    TableState.__EMPTY_BLOCK__ = 'x'

    initial_state = TableState('13 9 4 5 10 3 7 14 12 2 11 x 1 8 6 15', None)

    try:
        start = datetime.now()
        print_results(solve_puzzle(initial_state))
        print 'Puzzle solved in: ' + str((datetime.now() - start))
    except Exception as e:
        print e