from test import Board, drop


class TestDrop:
    def test_drop_check_stop_goal(self) -> None:
        """" Tests drop when stop is goal and multiple laps are made."""
        board = Board(6, 2)
        drop(board, 6)
        assert board.get_stop() == 1

    def test_drop_check_stop_not_goal(self) -> None:
        """" Tests drop when stop is not the goal."""
        board = Board(6, 2)
        drop(board, 4)
        assert board.get_stop() == 6


if __name__ == '__main__':
    import pytest
    pytest.main(['main_tests.py'])

