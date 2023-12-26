import unittest

from classes.window import Maze

class Test(unittest.TestCase):
    def test_maze_create_cells_correctly(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0,0,num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_rows,
            'Wrong number of rows created'
        )

        self.assertEqual(
            len(m1._cells[0]),
            num_cols,
            'Wrong number of cols created'
        )

        
    def test_maze_entry_and_exit_broken(self):
        maze = Maze(0,0, 3, 3, 10, 10)
        self.assertEqual(
            maze._cells[0][0].has_left_wall,
            False,
            "Entry has left wall"
        )

        self.assertEqual(
            maze._cells[0][0].has_top_wall,
            False,
           "Entry has top wall"
        )

        self.assertEqual(
            maze._cells[0][0].has_right_wall,
            False,
            "Entry has right wall"
        )

        self.assertEqual(
            maze._cells[0][0].has_bottom_wall,
            False,
            "Entry has bottom wall"
        )

        self.assertEqual(
            maze._cells[-1][-1].has_left_wall,
            False,
            "exit has left wall"
        )

        self.assertEqual(
            maze._cells[-1][-1].has_top_wall,
            False,
           "exit has top wall"
        )

        self.assertEqual(
            maze._cells[-1][-1].has_right_wall,
            False,
            "exit has right wall"
        )

        self.assertEqual(
            maze._cells[-1][-1].has_bottom_wall,
            False,
            "exit has bottom wall"
        )



    def test_maze_cannot_create_without_cells(self):
        # test for cell count by cols
        start_x = 0
        start_y = 0

        num_cols = 0 #invalid
        num_rows = 12 

        size_x = 5
        size_y = 10
        
        self.assertRaises(
            ValueError,
            Maze, start_x, start_y, num_rows, num_cols, size_x, size_y
        )
        
        # test by rows
        num_cols = 12 
        num_rows = 0  # invalid
        
        self.assertRaises(
            ValueError,
            Maze, start_x, start_y, num_rows, num_cols, size_x, size_y
        )

        # Test for cell size
        num_cols = 10
        num_rows = 12

        size_x = 0 # invalid
        size_y = 10
        self.assertRaises(
            ValueError,
            Maze, start_x, start_y, num_rows, num_cols, size_x, size_y
        )

        size_x = 10 
        size_y = 0
        self.assertRaises(
            ValueError,
            Maze, start_x, start_y, num_rows, num_cols, size_x, size_y
        ) 

    def test_maze_cannot_create_out_of_bounds(self):

        num_rows = 10
        num_cols = 20

        # test if x,y in canvas bounds negative
        x = 0
        y = -12

        self.assertRaises(
            ValueError,
            Maze, x, y, num_rows, num_cols, 10, 10
        )

        x = -10
        y = 0
        self.assertRaises(
            ValueError,
            Maze, x, y, num_rows, num_cols, 10, 10
        )


        x= -10
        y = -50
        self.assertRaises(
            ValueError,
            Maze, x, y, num_rows, num_cols, 10, 10
        )
if __name__ == "__main__":
    unittest.main()
