import scrabble_best_move as sc

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        input_file = sys.argv[1].strip()
    else:
        print('Please specify the input file')
        exit()

    sc.play(input_file, "resources/dict.txt")


