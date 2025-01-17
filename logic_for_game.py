import doctest

class Slot:
    """A slot in a Mancala board including goal as a slot

    Attributes:
        _pebbles: number of pebbles in the slot
        _next: next slot in the board
    """
    _pebbles: int
    _next: 'Slot'

    def __init__(self, num: int) -> None:
        """Initializes a slot with num of pebbles

        >>> slot = Slot(4)
        >>> slot.get_pebbles()
        4
        >>> slot.next() is None
        True
        """
        self._pebbles = num
        self._next = None

    def get_pebbles(self) -> int:
        return self._pebbles

    def set_pebbles(self, pebbles: int) -> None:
        self._pebbles = pebbles

    def drop_single_pebble(self) -> None:
        """Adds a single pebble in the slot"""
        self._pebbles += 1

    def pickup_all_pebbles(self) -> int:
        """Returns number of pebbles removed and removes all pebbles from the slot

        >>> slot = Slot(4)
        >>> slot.pickup_all_pebbles()
        4
        >>> slot.get_pebbles()
        0
        """
        pebbles = self._pebbles
        self._pebbles = 0
        return pebbles

    def next(self) -> 'Slot':
        """Returns the next slot in the board moving clockwise"""
        return self._next

class Slots:
    """A circular random aceess linked list with all the slots in a Mancala board.

    Attributes:
        goal: goal slot in the board with index 0
        _indexs: a dictionary mapping index to slot
    """
    goal: Slot
    _indexs: dict

    def __init__(self, length: int, pebbles_per_slot: int) -> None:
        """Initializes a board with length slots excluding goal with pebbles_per_slot pebbles in each slot

        preconditions:
            length > 0 and length // 2 == 0
            pebbles_per_slot > 0

        >>> slots = Slots(6, 4)
        >>> len(slots)
        6
        >>> slots.goal.get_pebbles()
        0
        >>> slots[6].get_pebbles()
        4
        >>> slots[0].next().get_pebbles()
        4
        >>> slots[6].next().get_pebbles()
        0
        """
        self._indexs = {}
        self.goal = Slot(0)
        self._indexs[0] = self.goal
        prev = self.goal
        for i in range(1, length + 1):
            slot = Slot(pebbles_per_slot)
            self._indexs[i] = slot
            prev._next = slot
            prev = slot
        prev._next = self.goal

    def __getitem__(self, index: int) -> Slot:
        return self._indexs[index]

    def __len__(self) -> int:
        return len(self._indexs) - 1

class Board:
    """ A mancala board

    Attributes:
        _slots: slots in the board
        _start: starting slot index
        _stop: ending slot index
        _hand: number of pebbles in hand which is then number pebbles picked up and not yet dropped
    """
    _slots: Slots
    _start: int
    _stop: int
    _hand: int

    def __init__(self, length: int, pebbles_per_slot: int) -> None:
        """Initializes a board with length slots excluding goal with pebbles_per_slot pebbles in each slot

        preconditions:
            length > 0
            pebbles_per_slot > 0 and length // 2 == 0

        >>> board = Board(6, 4)
        >>> board[6].get_pebbles()
        4
        >>> board._start is None
        True
        >>> board._stop is None
        True
        >>> board.get_hand()
        0
        """
        self._slots = Slots(length, pebbles_per_slot)
        self._start = None
        self._stop = None
        self._hand = 0

    def get_start(self) -> int:
        return self._start

    def set_start(self, start: int) -> None:
        """
        preconditions:
        """
        self._start = start

    def get_stop(self) -> int:
        return self._stop

    def set_stop(self, stop: int) -> None:
        """
        preconditions:
            stop must be a valid index in the board
        """
        self._stop = stop

    def get_hand(self) -> int:
        return self._hand

    def set_hand(self, hand: int) -> None:
        self._hand = hand

    def score(self) -> int:
        """Returns the score or number of pebbles in the goal slot

        >>> board = Board(6, 4)
        >>> board.score()
        0
        >>> board[0].drop_single_pebble()
        >>> board.score()
        1
        """
        return self._slots.goal.get_pebbles()

    def __getitem__(self, index: int) -> Slot:
        return self._slots[index]

    def __len__(self) -> int:
        return len(self._slots)

class Move:
    """ A node in a tree representing the end state after choosing the initial slot
    and moving the pebbles till the hand runs out into the goal or empty slot. This allows
    for the Move to represent the next choice the player makes on which slot to pick up next.

    Attributes:
        board: board after the move
        parent: the move from which this move was made
        childern: a list of moves are made next
    """
    board: Board
    _parent: 'Move'
    _children: list['Move']

    def __init__(self, board: Board) -> None:
        self.board = board
        self._parent = None
        self._children = []

    def add_child(self, child: 'Move') -> None:
        self._children.append(child)
        child._parent = self

    def get_parent(self) -> 'Move':
        return self._parent

    def get_children(self) -> list['Move']:
        return self._children

    def get_score(self) -> int:
        return self.board.score()

    def open_moves(self) -> list:
        """Reutrns a list of slots in the board that can be starting moves

        >>> board = Board(6, 4)
        >>> move = Move(board)
        >>> move.open_moves()
        [4, 5, 6]
        >>> board[4].set_pebbles(0)
        >>> move.open_moves()
        [5, 6]
        """
        posible_moves = []
        for i in range((len(self.board) // 2) + 1, len(self.board) + 1):
            if self.board[i].get_pebbles() > 0:
                posible_moves.append(i)
        return posible_moves

    def get_start(self) -> int:
        return self.board.get_start()

def drop(board: Board, start: int) -> None:
    """Updates board with a turn picking up pebbles from start slot and dropping them till hand runs out.
    Start is not updated

    preconditions:
        start must be a valid index in the board meaning
        board[start].get_pebbles() > 0

    >>> board = Board(6, 2)
    >>> drop(board, 5)
    >>> board[5].get_pebbles()
    0
    >>> board[6].get_pebbles()
    3
    >>> board[0].get_pebbles()
    1
    >>> board.get_hand()
    0
    >>> board.get_start()
    5
    >>> board.get_stop()
    0
    """
    hand = board[start].pickup_all_pebbles()
    board.set_start(start)
    current = board[start]
    stop = start
    while hand > 0:
        stop += 1
        current = current.next()
        current.drop_single_pebble()
        hand -= 1
    board.set_stop(stop % (len(board) + 1))

def play_turn(board: Board, start: int) -> None:
    """ Updates board to relfect a turn starting at start slot.

    preconditions:
        start must be a valid index in the board meaning
        board[start].get_pebbles() > 0

    >>> board = Board(6, 2)
    >>> play_turn(board, 6)
    >>> board[6].get_pebbles()
    1
    >>> board[0].get_pebbles()
    2
    >>> board[4].get_pebbles()
    0
    >>> board.get_start()
    6
    >>> board.get_stop()
    0
    """
    drop(board, start)
    board.set_start(board.get_stop())
    while board.get_stop() != 0 and board[board.get_stop()].get_pebbles != 1:
        drop(board, board.get_start())
        board.set_start(board.get_stop())
    board.set_start(start)

def simulate_game(move: Move) -> Move:
    """ Returns best final turn and updates the move tree with all trials before.
    There maybe a starting move that earns more points, but the first one that
    wins the game is returned or the best one.

    >>> board = Board(6, 2)
    >>> move = Move(board)
    >>> final_move = simulate_game(move)
    >>> final_move.get_score()
    5
    >>> final_move.get_parent().get_parent().board == board
    True
    >>> final_move.board != board
    True
    """
    child_index = 0
    best_move = move
    best_move_score = diff_goal_board(move)
    for i in move.open_moves():
        new_node = Move(move.board)
        play_turn(new_node.board, i)
        move.add_child(new_node)
        if diff_goal_board(move.get_children()[child_index]) > 0:
            return move.get_children()[child_index]
        elif diff_goal_board(move.get_children()[child_index]) > best_move_score:
            best_move = move.get_children()[child_index]
            best_move_score = diff_goal_board(move.get_children()[child_index])
        else:
            simulate_game(move.get_children()[child_index])
        child_index += 1
    return best_move

def does_guarantee_win(move: Move) -> bool:
    """Returns True if the move guarantees a win"""
    return diff_goal_board(move) > 0

def print_move(move_tree: Move, move: Move) -> None:
    """Prints the path ending at move from move_tree.

    Precondition:
        move is in move_tree
    """
    move_stack = []
    while move.get_parent() is not None:
        move_stack.append(move)
        move = move.get_parent()

    while len(move_stack) != 0:
        current = move_stack.pop()
        print(f"pick up {current.get_start()} so the score will be {current.get_score()}")

def diff_goal_board(move: Move) -> int:
    """Returns (number of pieces in the goal) - (number of pieces left in the board).

    >>> board = Board(6, 2)
    >>> move = Move(board)
    >>> diff_goal_board(move)
    -12
    >>> board[0].set_pebbles(3)
    >>> diff_goal_board(move)
    -9
    """
    pieces_left = 0
    for i in range(1, len(move.board) + 1):
        pieces_left += move.board[i].get_pebbles()
    return move.get_score() - pieces_left
