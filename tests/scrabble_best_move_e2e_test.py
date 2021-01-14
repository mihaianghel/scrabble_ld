import unittest
import os
from context import scrabble_best_move as sb


class Scrabble_Best_Move_E2E_Test(unittest.TestCase):

    def test_play_e2e(self):
        # when
        result = sb.play(input_file="resources/input_test.txt",
                         dict_file='../resources/dict.txt')

        # open th file resulted from the execution and assert result
        file = open('resources/input_test.txt.answer')
        for line in file:
            self.assertEquals(line, '(11, 7, true, ducat)')

        # cleanup
        os.remove('resources/input_test.txt.answer')

if __name__ == '__main__':
    unittest.main()
