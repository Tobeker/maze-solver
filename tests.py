import unittest
from maze import Maze

class MockWindow:
    def redraw(self):
        pass

    def draw_line(self, line, fill_color):
        pass

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        mock_win = MockWindow()

        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, mock_win)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_entrance_exit_cells(self):
        num_cols = 12
        num_rows = 10
        mock_win = MockWindow()

        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, mock_win)
        self.assertEqual(
            m1._cells[0][0].has_top_wall,
            False,
        )
        self.assertEqual(
            m1._cells[num_cols - 1][num_rows - 1].has_bottom_wall,
            False,
        )

if __name__ == "__main__":
    unittest.main()