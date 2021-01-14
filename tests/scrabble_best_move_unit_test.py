import unittest
import numpy as np
from context import scrabble_best_move as sb


class Scrabble_Best_Move_Unit_Test(unittest.TestCase):

    def test_find_highest_scoring_words(self):
        # given
        available_tiles = 'arcxd'
        dictionary = {'aa': ['aa'],
                      'acr': ['car', 'arc'],
                      'dgo': ['dog'],
                      'acdr': ['card', 'darc']}

        # when
        result = sb.find_highest_scoring_words(available_tiles, dictionary)

        # then
        self.assertEqual(result[0][0], 'car')
        self.assertEqual(result[0][1], 5)
        self.assertEqual(result[1][0], 'arc')
        self.assertEqual(result[1][1], 5)
        self.assertEqual(result[3][0], 'darc')
        self.assertEqual(result[3][1], 7)

    def test_get_words_from_the_board(self):

        # given
        board = [['-', '-', '-', 'c', '-'],
                 ['-', 'm', '-', 'a', '-'],
                 ['t', 'e', 's', 't', '-'],
                 ['-', 'n', '-', '-', '-'],
                 ['-', '-', '-', '-', '-']]

        # when
        horizontal_words = sb.get_words_from_the_board(board, True)
        vertical_words = sb.get_words_from_the_board(np.array(board).transpose(), False)

        # then
        self.assertEqual(len(horizontal_words), 1)
        self.assertEqual(horizontal_words[0]['word'], 'test')
        self.assertEqual(len(vertical_words), 2)
        self.assertEqual(vertical_words[0]['word'], 'men')
        self.assertEqual(vertical_words[1]['word'], 'cat')

    def test_get_best_move_one_move_vertical(self):

        # Horizontal word top left
        # given
        wor = [('cider', 2)]
        wob = [{'word': 'car', 'x': 1, 'y': 0, 'is_horizontal': True}]
        dictionary = {'acir': ['icar', 'cari']}
        board = [['-', '-', '-', '-', '-'],
                 ['c', 'a', 'r', '-', '-'],
                 ['-', '-', '-', '-', '-'],
                 ['-', '-', '-', '-', '-'],
                 ['-', '-', '-', '-', '-']]

        # when
        result = sb.get_best_move(board, wor, wob, dictionary)

        # then
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['x'], 0)
        self.assertEqual(result[0]['y'], 3)

    def test_get_best_move_collision(self):

        # Horizontal word top left
        # given
        wor = [('cider', 2)]
        wob = [{'word': 'car', 'x': 1, 'y': 0, 'is_horizontal': True}]
        dictionary = {'acir': ['icar', 'cari']}
        board = [['-', '-', '-', '-', '-'],
                 ['c', 'a', 'r', '-', '-'],
                 ['-', 'r', '-', '-', '-'],
                 ['-', 'm', '-', '-', '-'],
                 ['-', 'y', 'e', 's', '-']]

        # when
        result = sb.get_best_move(board, wor, wob, dictionary)

        # then
        self.assertEqual(len(result), 0)

    def test_get_best_move_one_move_horizontal(self):
        # Vertical word bottom left
        # given
        wor = [('cider', 2)]
        wob = [{'word': 'car', 'x': 3, 'y': 2, 'is_horizontal': False}]
        dictionary = {'acir': ['icar', 'cari']}
        board = [['-', '-', '-', '-', '-', '-'],
                 ['-', '-', '-', '-', '-', '-'],
                 ['-', '-', '-', '-', '-', '-'],
                 ['-', '-', 'c', '-', '-', '-'],
                 ['-', '-', 'a', '-', '-', '-'],
                 ['-', '-', 'r', '-', '-', '-']]

        # when
        result = sb.get_best_move(board, wor, wob, dictionary)

        # then
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['x'], 2)
        self.assertEqual(result[0]['y'], 1)

    def test_get_best_move_no_move(self):

        # Horizontal word top left
        # given
        wor = [('cider', 2)]
        wob = [{'word': 'car', 'x': 1, 'y': 0, 'is_horizontal': True}]
        dictionary = {'acir': ['icar', 'cari']}
        board = [['-', '-', '-', '-'],
                 ['c', 'a', 'r', '-'],
                 ['-', '-', '-', '-'],
                 ['-', '-', '-', '-']]

        # when
        result = sb.get_best_move(board, wor, wob, dictionary)

        # then
        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main()
