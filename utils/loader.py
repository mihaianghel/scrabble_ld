import utils.helper as helper

#
# Contains methods used to load data from files stored on the disk
#


# Creates a mapping between the sequence of characters and all anagrams for that sequence
# ex: <'acr', ['car', 'arc']>
def load_dictionary(filename):
    file = open(filename)
    anagrams = {}
    for word in file:
        word = word.strip()
        # sorted() returns a list of sorted characters hence join()
        sorted_word = ''.join(sorted(word))
        if sorted_word in anagrams:
            anagrams[sorted_word].append(word)
        else:
            anagrams[sorted_word] = [word]
    file.close()
    return anagrams


# Returns the state of the board as a 2D array and the available tiles
def load_current_game_state_and_validate_input(filename):
    tiles = ''
    board = [[0 for i in range(15)] for j in range(15)]
    x = 0
    file = open(filename)
    for line in file:
        line = line.strip()
        # rack line
        if x == 15:
            tiles = line
            helper.validate_rack(tiles)
            break
        # too many lines
        elif x > 16:
            raise Exception('Invalid size of the board')
        y = 0
        # first 15 lines
        for c in line:
            helper.validate_size_of_board(line)
            helper.validate_characters(c)
            board[x][y] = c
            y = y + 1
        x = x + 1
    game_state = {
        "board": board,
        "tiles": tiles
    }
    return game_state