# see http://www.bananagrammer.com/2013/10/the-boggle-cube-redesign-and-its-effect.html

import random
import numpy as np
from typing import LiteralString


def read_dictionary(dictionaryname="scrabble_official_enable1.txt"):
    words = []
    with open(dictionaryname) as fp:
        words = fp.readlines()
        words = [word.rstrip('\n') for word in words]
        words = [word for word in words if len(word)>2] #legal boggle words have length 3 or more
        print(f'{len(words)} legal boggle words in dictionary {dictionaryname}')
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
            words = find_words_from_here(letter_matrix,(i,j),word_so_far='')
            print(f'words starting from {i},{j}:{words}')
            all_words+=words   # this should have a check for dupes. Or de-dupe at end
    return all_words


die_used_in_word=('\0')
def find_words_from_here(letter_matrix,position,word_so_far):
    '''
    :param letter_matrix:
    :param position:
    :param word_so_far:
    :return:
    '''
    current_matrix = [[l for l in row] for row in letter_matrix]
    allwords = []
    current_word=None
    [i,j] = position
    if current_matrix[i][j] == die_used_in_word:
        return []
    neighbors = [[i-1,j-1],[i,j-1],[i+1,j-1],[i-1,j],[i+1,j],[i-1,j+1],[i,j+1],[i+1,j+1]]  #all nearest neighbors inc. diagonals
    neighbors = [neighbor for neighbor in neighbors if neighbor[0]>=0 and neighbor[0]<4 and neighbor[1]>=0 and neighbor[1]<4 ]
    word_so_far += current_matrix[i][j]
    current_matrix[i][j]=die_used_in_word
    if not can_word_start_like_this(word_so_far):
        return []
    if word_so_far.lower() in LEGAL_WORDS:
        allwords.append( word_so_far)
    for neighbor in neighbors:
        words = find_words_from_here(current_matrix,neighbor,word_so_far)
        for word in words:
            if not word in allwords:
                allwords.append(word)
    return allwords

def can_word_start_like_this(word_so_far):
    # this check should kick out words that can't possibly begin like this
    # currently pretty inefficient  , there is prob. some smart way to do this
    # we already checked if the word itself is in the dictionary of legal words, so no need to check that
    l = len(word_so_far)
    word_beginnings_of_greater_length = [word[0:l] for word in LEGAL_WORDS if len(word)>l]
    if word_so_far.lower() in word_beginnings_of_greater_length:
        return True
    return False

def board_stats():

    all_results=[]
    while(1):
        board = generate_boggleboard(STANDARD_DIES)
        print_board(board)
        n_words=len(find_words(board))
        all_results.append(n_words)
        avg = np.mean(all_results)
        std = np.std(all_results)
        min = np.min(all_results)
        max = np.max(all_results)
        print(f'n words {n_words} avg {avg} std {std}')
        print_board(board)
        with open('most_prolific_board.txt','a') as fp:
            fp.write(f'n_words {n_words} avg {avg} std {std} min {min} max {max} N {len(all_results)} board:\t')
            for row in range(4):
                for col in range(4):
                    fp.write(f'{board[row][col]}\t')
                fp.write('')
            fp.write('\n')
            fp.close()

STANDARD_DIES = [
        ['A','A','E','E','G','N'],
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

LEGAL_WORDS = read_dictionary()

board_stats()
board = generate_boggleboard(STANDARD_DIES)
board = [['R',	'I',	'E',	'L'],
['A',	'Qu',	'D',	'E'	],
['T'	,'V',	'R',	'P'],
['O',	'C',	'I',	'T'	]]
print_board(board)
found_words = find_words(board)
print(found_words)
