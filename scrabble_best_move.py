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


def get_words_from_the_board(board, isHorizontal):
    x = 0
    words_on_board = []
    # visit rows
    for row in board:
        row_str = (''.join(row))
        for w in re.split('-+', row_str):
            if len(w) > 1:
                if isHorizontal:
                    x_coord = x
                    y_coord = row_str.find(w)
                else:
                    y_coord = x
                    x_coord = row_str.find(w)
                w_on_board = {
                        "word": w,
                        "x": x_coord,
                        "y": y_coord,
                        "isHorizontal": isHorizontal
                }
                words_on_board.append(w_on_board)
        x = x + 1
    return words_on_board


def get_best_move(words_on_rack, words_on_board, dictionary):

    good_words = []

    for wob in words_on_board:
        for wor in words_on_rack:
            x = 0  # index of the character in wor
            for c in wor[0]:

                # potential new word formed by a letter from rack prefixed to a word on board
                new_word = c + wob['word']
                # if new word in the dictionary
                key_in_dictionary = ''.join(sorted(new_word))
                if (key_in_dictionary in dictionary) and (new_word in dictionary[key_in_dictionary]):
                    # check the word on rack fits on the board to form new_word
                    if wob['isHorizontal']:
                        if not((wob["y"] == 0) or (wob["x"] < x) or ((14 - wob["x"]) < len(wor[0]) - 1 - x)):
                            # word fits on the left vertically
                            good_words.append({
                                'word': wor[0],
                                'score': wor[1] + helper.get_score(new_word),
                                'isHorizontal': True,
                                'x': wob["x"] - x,
                                'y': wob["y"] - 1
                            })
                    else:
                        if not((wob["x"] == 0) or (wob["y"] < x) or ((14 - wob["y"]) < len(wor[0]) - 1 - x)):
                            # word fits on the top horizontally
                            good_words.append({
                                'word': wor[0],
                                'score': wor[1] + helper.get_score(new_word),
                                'isHorizontal': False,
                                'x': wob["x"] - 1,
                                'y': wob["y"] - x
                    })

                # potential new word formed by a letter from rack suffixed to a word on board
                new_word = wob['word'] + c
                # if new word in the dictionary
                key_in_dictionary = ''.join(sorted(new_word))
                if (key_in_dictionary in dictionary) and (new_word in dictionary[key_in_dictionary]):
                    # check the word on rack fits on the board to form new_word
                    if wob['isHorizontal']:
                        if not(((wob["y"] + len(wob['word']) - 1) >= 14) or (wob["x"] < x) or ((14 - wob["x"]) < len(wor[0]) - 1 - x)):
                            # word fits on the right vertically
                            good_words.append({
                                'word': wor[0],
                                'score': wor[1] + helper.get_score(new_word),
                                'isHorizontal': True,
                                'x': wob["x"] - x,
                                'y': (wob["y"] + len(wob['word']))
                            })
                    else:
                        if not(((wob["x"] + len(wob['word']) - 1) >= 14) or (wob["y"] < x) or ((14 - wob["y"]) < len(wor[0]) - 1 - x)):
                            # word fits on the right vertically
                            good_words.append({
                                'word': wor[0],
                                'score': wor[1] + helper.get_score(new_word),
                                'isHorizontal': False,
                                'x': (wob["x"] + len(wob['word'])),
                                'y': wob["y"] - x
                            })

                x = x + 1
    return good_words


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
    candidate_words = get_best_move(valid_words, horizontal_wob + vertical_wob, dictionary)
    best_move = {"score": 0}
    for w in candidate_words:
        if w["score"] >= best_move["score"]:
            best_move = w;

    # Print output file in the format (13,1,true,yay)
    f = open(input_file + '.answer', 'w')
    result = str((best_move["x"], best_move["y"], not(best_move["isHorizontal"]), best_move["word"])).lower().replace("'", "")
    f.write(result)
    f.close()

    print(result)


