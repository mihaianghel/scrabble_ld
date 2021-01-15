from itertools import combinations
import utils.loader as loader
import utils.helper as helper
import numpy as np
import re as re


def find_highest_scoring_words(available_tiles, dictionary):
    tiles = ''.join(sorted(available_tiles))
    valid_words = {}
    for i in range(2, len(tiles)+1):
        # create combinations of 2,3...7 letters from the available tiles
        for combination in combinations(tiles, i):
            sorted_combination = ''.join(sorted(combination))
            if sorted_combination not in dictionary:
                continue
            for w in dictionary[sorted_combination]:
                valid_words[w] = helper.get_score(w)

    # return a tuple sorted by the score of each word
    return sorted(valid_words.items(), key=lambda x: x[1])


def get_words_from_the_board(board, is_horizontal):
    x = 0
    words_on_board = []

    for row in board:
        row_str = (''.join(row))
        for w in re.split('-+', row_str):
            if len(w) > 1:
                if is_horizontal:
                    x_coord = x
                    y_coord = row_str.find(w)
                else:
                    y_coord = x
                    x_coord = row_str.find(w)
                w_on_board = {
                        "word": w,
                        "x": x_coord,
                        "y": y_coord,
                        "is_horizontal": is_horizontal
                }
                words_on_board.append(w_on_board)
        x += 1
    return words_on_board


def check_word_fits_on_board(board, x, y, word_len, is_horizontal):
    x_coord = x
    y_coord = y
    board_size = len(board) - 1

    for i in range(word_len):
        if x_coord < 0 or x_coord > board_size \
                or y_coord < 0 or y_coord > board_size \
                or board[x_coord][y_coord] != '-':
            return False
        if is_horizontal:
            y_coord += 1
        else:
            x_coord += 1
    return True


def get_best_move(board, words_on_rack, words_on_board, dictionary):

    words = []

    for wob in words_on_board:
        for wor in words_on_rack:
            x = 0  # index of the character in wor
            for c in wor[0]:

                #
                # Check if new_word fits on the left or on top, if the letter (c) is a prefix
                # for the word on the board (wob)
                #
                new_word = c + wob['word']
                # if new word in the dictionary
                key_in_dictionary = ''.join(sorted(new_word))
                if (key_in_dictionary in dictionary) and (new_word in dictionary[key_in_dictionary]):
                    if wob['is_horizontal']:
                        x_coord = wob["x"] - x
                        y_coord = wob["y"] - 1
                        if check_word_fits_on_board(board, x_coord, y_coord, len(wor[0]), False):
                            # word fits on the left vertically
                            words.append({'word': wor[0], 'score': wor[1] + helper.get_score(new_word),
                                          'is_horizontal': True, 'x': x_coord, 'y': y_coord})
                    else:
                        x_coord = wob["x"] - 1
                        y_coord = wob["y"] - x
                        if check_word_fits_on_board(board, x_coord, y_coord, len(wor[0]), True):
                            # word fits on the top horizontally
                            words.append({'word': wor[0],'score': wor[1] + helper.get_score(new_word),
                                          'is_horizontal': False, 'x': x_coord, 'y': y_coord})

                #
                # Check if new_word fits on the right or on the bottom, if the letter (c) is a suffix
                # for the word on the board (wob)
                #
                new_word = wob['word'] + c
                # if new word in the dictionary
                key_in_dictionary = ''.join(sorted(new_word))
                if (key_in_dictionary in dictionary) and (new_word in dictionary[key_in_dictionary]):
                    if wob['is_horizontal']:
                        x_coord = wob["x"] - x
                        y_coord = wob["y"] + len(wob['word'])
                        if check_word_fits_on_board(board, x_coord, y_coord, len(wor[0]), False):
                            # word fits on the left vertically
                            words.append({'word': wor[0], 'score': wor[1] + helper.get_score(new_word),
                                          'is_horizontal': True, 'x': x_coord, 'y': y_coord})
                    else:
                        x_coord = wob["x"] + len(wob['word'])
                        y_coord = wob["y"] - x
                        if check_word_fits_on_board(board, x_coord, y_coord, len(wor[0]), True):
                            # word fits on the bottom horizontally
                            words.append({'word': wor[0], 'score': wor[1] + helper.get_score(new_word),
                                          'is_horizontal': False, 'x': x_coord, 'y': y_coord})

                x += 1
    return words


def play(input_file, dict_file):

    # Initialise dictionary
    dictionary = loader.load_dictionary(dict_file)

    # Retrieve the current state of the game and rack
    game_state = loader.load_current_game_state_and_validate_input(input_file)
    board = game_state['board']
    tiles = game_state['tiles']

    # Calculate the highest scoring words from the rack
    valid_words = find_highest_scoring_words(tiles, dictionary)

    # Extract words on board (wob)
    horizontal_wob = get_words_from_the_board(board, True)
    vertical_wob = get_words_from_the_board(np.array(board).transpose(), False)

    # Calculate candidate words to place on board and pick the one with greatest score
    candidate_words = get_best_move(board, valid_words, horizontal_wob + vertical_wob, dictionary)
    best_move = {"score": 0}
    for w in candidate_words:
        if w["score"] >= best_move["score"]:
            best_move = w

    # Print output to file in the format (13,1,true,yay)
    f = open(input_file + '.answer', 'w')
    best_move = str((best_move["x"], best_move["y"], not(best_move["is_horizontal"]), best_move["word"])).lower().replace("'", "")
    f.write(best_move)
    f.close()

    return best_move
