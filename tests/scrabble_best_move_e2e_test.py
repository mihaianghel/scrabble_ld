import unittest
import os
from context import scrabble_best_move as sb


class Scrabble_Best_Move_E2E_Test(unittest.TestCase):

    def test_play_e2e_happy_path(self):
        # when
        result = sb.play(input_file="resources/valid_board.txt",
                         dict_file='../resources/dict.txt')

        # open th file resulted from the execution and assert result
        file = open('resources/valid_board.txt.answer')
        for line in file:
            self.assertEquals(line, '(11, 7, true, ducat)')

        # cleanup
        os.remove('resources/valid_board.txt.answer')

    def test_e2e_invalid_board_size_too_large(self):
        with self.assertRaises(Exception):
            sb.play(input_file="resources/invalid_board_large.txt",
                    dict_file='../resources/dict.txt')

    def test_e2e_invalid_board_size_too_small(self):
        with self.assertRaises(Exception):
            sb.play(input_file="resources/invalid_board_small.txt",
                    dict_file='../resources/dict.txt')

    def test_e2e_invalid_line_too_small(self):
        with self.assertRaises(Exception):
            sb.play(input_file="resources/invalid_board_line_short.txt",
                    dict_file='../resources/dict.txt')

    def test_e2e_invalid_tiles_on_board(self):
        with self.assertRaises(Exception):
            sb.play(input_file="resources/invalid_board_tiles.txt",
                    dict_file='../resources/dict.txt')

    def test_e2e_invalid_rack_size(self):
        with self.assertRaises(Exception):
            sb.play(input_file="resources/invalid_board_rack_size.txt",
                    dict_file='../resources/dict.txt')

    def test_e2e_invalid_rack_characters(self):
        with self.assertRaises(Exception):
            sb.play(input_file="resources/invalid_board_rack_characterstxt",
                    dict_file='../resources/dict.txt')


if __name__ == '__main__':
    unittest.main()
