#
# Contains helper methods
#

points = {"e": 1, "a": 1, "i": 1, "o": 1, "n": 1,
          "s": 1, "r": 1, "u": 1, "t": 1, "l": 1,
          "d": 2, "g": 2,
          "b": 3, "c": 3, "m": 3, "p": 3,
          "f": 4, "h": 4, "w": 4, "v": 4, "y": 4,
          "k": 5,
          "x": 8, "j": 8,
          "q": 10, "z": 10}


def validate_characters(c):
    if not (c == '-' or c.isalpha()):
        print('Invalid characters on the board')
        exit()


def validate_size_of_board(line):
    if len(line) != 15:
        print('Invalid size of the board')
        exit()


def validate_size_of_rack(tiles):
    if len(tiles) != 7:
        print('Invalid size of the rack')
        exit()


def get_score(word):
    values = []
    for c in word:
        values.append(points[c])
    return sum(values)
