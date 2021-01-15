import sys
import scrabble_best_move as sc


def main(argv):
    if len(argv) == 2:
        input_file = argv[1].strip()
    else:
        print('Please specify the input file')
        exit()

    best_move = sc.play(input_file, "resources/dict.txt")
    print(best_move)


if __name__ == "__main__":
    main(sys.argv)
