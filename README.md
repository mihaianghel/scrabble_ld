Scrabble Best Move Simulator
=========

Getting Started
---------------
You need Python 3 to run the Scrabble Best Move Simulator. The code was tested on Python v3.9. Make sure it's installed 
by running `python3` in the command line, and you should be directed to the python console. 
To exit type `exit()`.

Additional libraries to install:
* numpy - run `pip3 install numpy`

A dictionary of permitted words, is located at *resources/dict.txt*. This is the implicit dictionary used when starting a game.

The mandatory parameter to be passed as an argument when simulating the highest scoring move is the input file which captures 
the current state of the Scrabble board. To start the game run:
```shell
python3 play.py resources/input.txt
```

This will return the result in the format below. The first two numbers represent the starting coordinates of the word, 
the boolean flag is true if the word is vertical, and the fourth value is the highest scoring word.
```text
(13,1,true,yay)
```

Also, part of running the `play.py` script an `*.answer` file will be generated in the folder of your input script.

Tests
-----
Due to time constraints, a limited set of tests has been added in the `tests` folder. For a production ready application, 
  a more through testing strategy should be adopted.
  
To run the unit tests:
```shell
python3 tests/scrabble_best_move_unit_test.py
```
To run e2e tests:
```shell
cd tests && python3 scrabble_best_move_e2e_test.py
```

Approach for the implementation
-------------------------------

1. The file `dict.txt` is loaded from the memory, and a map of anagrams is built. One entry in the map could look like
   `{'acr': ['car', 'arc']}` assuming that `car` and `arc` are valid words in the dictionary.
2. Load the state of the game from the output file. This creates a `board` structure and a `tiles` structure with acts as the
   rack of tiles.
3. Using the rack of 7 tiles, combinations of 2,3...7 letters are created (120) and checked against the dictionary if there 
   are any valid words to be created. An array of tuples `[(word, score)]` is created.
4. Traverse the board and extract the horizontal & vertical word in the format 
   `{'word': 'car', 'x': 4, 'y': 5, 'is_horizontal': True}`
5. Using the data structures from step 3 & 4, every combination of words is tested so that each word on the rack will be 
   placed perpendicularly on each word on the board and shifted left-to-right (for vertical words) and top-to-bottom 
   (for horizontal words) trying to get a higher score by scoring on two words: the added word, and a newly created using 
   the one on the board.
6. The highest scoring combination of words will be printed to the `*.answer` file.   

Assumptions
-----------
* In order to reduce the complexity of the implementation it is assumed that to produce a high scoring move, 
  the added word has to be perpendicularly adjacent to an existing word on the board so that one of the letters of the 
  added word would contribute to the creation of a new word based on the previously existing word on the board. Hence 2 
  words would contribute to the overall score.
  
* Tiles only contain letters

* Empty squares on the board are represented by the `-` (dash) character

Caveats
-------
* Words are only added at the beginning or end of existing words on the board to maximise the score. If there is no move 
  with this constraint, no move is returned.

