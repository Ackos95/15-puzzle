__author__ = 'Acko'

from application.Heap import Heap


class NotSolvablePuzzle(Exception):
    """ Exception derived class """

    pass


def solve_puzzle(initial_state):
    """
        Function which finds 15-puzzle solution, based on A* algorithm.

        Each move is represented with TableState instance, priority_queue used for A* algorithm is actually heap,
        and list of already checked nodes (moves) is actually dictionary (can do this because of overloaded __hash__
        method in TableState).

        :param initial_state: (TableState) state of puzzle which should be solved
        :return: (TableState) state of solved puzzle (with parent information which can lead to starting point)
    """

    if not initial_state.is_solvable():
        raise NotSolvablePuzzle("Puzzle not solvable!")

    priority_queue = Heap(Heap.HEAP_DOWN)
    priority_queue.add(initial_state.manhattan(), initial_state)

    already_checked = {}

    current_state = None
    while not priority_queue.is_empty():
        current_state = priority_queue.pop()[1]

        if current_state.is_final():
            break

        already_checked[current_state] = True

        for next_state in current_state.generate_next_moves():
            if already_checked.get(next_state):
                continue
            priority_queue.add(next_state.manhattan(), next_state)

    return current_state


def print_results(final_state):
    """
        Method created only to print results, based on final puzzle state (TableState instance)

        :param final_state: (TableState) state of solved puzzle (with parent information which lead to beginning)
    """

    result_path = []
    while final_state is not None:
        result_path.append(final_state)
        final_state = final_state.parent

    for i in xrange(len(result_path) - 1, -1, -1):
        print result_path[i]

    print 'Solved in ' + str(len(result_path)) + ' moves'