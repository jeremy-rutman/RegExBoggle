# see http://www.bananagrammer.com/2013/10/the-boggle-cube-redesign-and-its-effect.html

import random
from ftplib import all_errors


def read_dictionary(dictionaryname="scrabble_official_enable1.txt"):
    words = []
    with open(dictionaryname) as fp:
        words = fp.readlines()
        words = [word.rstrip('\n') for word in words]
        return words

def generate_boggleboard(dies):
    '''
    :param dies: list of dies. Each die is a length-6 list of letters/symbols
    :return: list of die values in order, like first one is the top left , fourth is top right etc.
    '''
    n_dies = len(dies)
    die_locations = [i for i in range(n_dies)] #indices for die locations
    random.shuffle(die_locations)
    die_values = [dies[die_location][random.randint(0,5)] for die_location in die_locations]
    letter_matrix = [[die_values[i+4*j] for i in range(4)] for j in range(4)]

    return letter_matrix


def print_board(letter_matrix):
    for row in range(4):
        for col in range(4):
           print(f'{letter_matrix[row][col]}\t',end='')
        print('')

def find_words(letter_matrix):
    board_size = len(letter_matrix[0]) # size of a row
    all_words = []
    for i in range(board_size):
        for j in range(board_size):
            words = find_words_starting_here(letter_matrix,(i,j))
            all_words.append(words)
    return all_words


die_used_in_word=('\0')
def find_words_starting_here(letter_matrix,position):
    [i,j] = position
    neighbors = [[i-1,j-1],[i,j-1],[i+1,j-1],[i-1,j],[i+1,j],[i-1,j+1],[i,j+1],[i+1,j+1]]  #all nearest neighbors inc. diagonals
    neighbors = [neighbor for neighbor in neighbors if neighbor[0]>=0 and neighbor[0]<4 and neighbor[1]>=0 and neighbor[1]<4 ]


standard_dies = [['A','A','E','E','G','N'],
        ['A','B','B','J','O','O'],
        ['A','C','H','O','P','S'],
        ['A','F','F','K','P','S'],
        ['A','O','O','T','T','W'],
        ['C','I','M','O','T','U'],
        ['D','E','I','L','R','X'],
        ['D','E','L','R','V','Y'],
        ['D','I','S','T','T','Y'],
        ['E','E','G','H','N','W'],
        ['E','E','I','N','S','U'],
        ['E','H','R','T','V','W'],
        ['E','I','O','S','S','T'],
        ['E','L','R','T','T','Y'],
        ['H','I','M','N','U','Qu'],
        ['H','L','N','N','R','Z']]


words = read_dictionary()
board = generate_boggleboard(standard_dies)
print_board(board)
find_words(board)
