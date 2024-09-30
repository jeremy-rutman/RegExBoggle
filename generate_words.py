# see http://www.bananagrammer.com/2013/10/the-boggle-cube-redesign-and-its-effect.html
# 10:23 at n=11 10:29 n19 10:32 n26  restart 10:42
import random
import numpy as np
import re
from typing import LiteralString

REGEX_CHARS = ['-','.','*']

def read_dictionary(dictionaryname="scrabble_official_enable1.txt"):
    words = []
    with open(dictionaryname) as fp:
        words = fp.readlines()
        words = [word.rstrip('\n') for word in words]
        words = [word for word in words if len(word)>2] #legal boggle words have length 3 or more
        words = set(words) # 'if x in set(list)' is apparently indexed and hence much faster than 'if x in list'
        print(f'{len(words)} legal boggle words in dictionary {dictionaryname}')
        return words

LEGAL_WORDS = read_dictionary()

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
            for word in words: # check for dupes. Or de-dupe at end
                word = word.lower()
                if not word in all_words:
                    all_words.append(word)
    all_with_regex = regex_matches_to_all_matches(all_words)
    return all_with_regex


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
    if is_this_a_legal_word(word_so_far):   #this may be slower than gathering all potential words and then using set.intersection
        allwords.append( word_so_far)
    for neighbor in neighbors:
        words = find_words_from_here(current_matrix,neighbor,word_so_far)
        for word in words:
            if not word in allwords:
                allwords.append(word)
    return allwords

def is_this_a_legal_word(word_so_far):
    '''
    #todo deal with consecutive hyphens , i guess illegal
    :param word_so_far:
    :return:
    '''
    # for testing purposes
    if len(word_so_far)>8:
        return False
    if not(set.intersection(set(REGEX_CHARS),set(word_so_far))):   #no regex chars
        if (word_so_far).lower() in LEGAL_WORDS:
            return True
        return False
    # at least 5 chars for a hyphen regex like AB-CD
    if '-' in word_so_far:
        if len(word_so_far) < 5:
            return False
        positions = [pos for pos, char in enumerate(word_so_far) if char == '-']
        # is last char a '-' , if so not a word
        if positions[-1] == len(word_so_far):
            return False
        # is first char a hyphen, if so not legal word
        if positions[0] == 0:
            return False
    regex_str = transform_to_legal_regex(word_so_far)
    if not regex_str: #no possible regex ilke this
        return False
    regex_str = r'^' + regex_str + r'$'
    myregex = re.compile(regex_str)
    for word in LEGAL_WORDS:
        if myregex.match(word):
#            print(f'{word} matches {regex_str}')
            return True
    return False

def regex_matches_to_all_matches(wordlist): # this is zach's phase 2
    allwords = []
    print(f'incoming wordlist:{wordlist}')
    for word in wordlist:
        if not (set.intersection(set(REGEX_CHARS), set(word))):  # no regex chars
            allwords.append(word.lower())
            continue
        regex_str = transform_to_legal_regex(word)
        if not regex_str:  # no possible regex ilke this
            print('this should not happen')
        regex_str = r'^' + regex_str + r'$'
        myregex = re.compile(regex_str)
        for mword in LEGAL_WORDS:
            if myregex.match(mword):
  #              print(f'{mword} matches {regex_str} .')
                if not mword in allwords:
                    allwords.append(mword)
    allwords = list(set(allwords)) # there are still duplicates showing up somehow, this removes them
    allwords=sorted(allwords)
    print(f'outgoing wordlist:{allwords}')
    return allwords

def transform_to_legal_regex(word_so_far):
    regex_str = word_so_far
    if '-' in word_so_far:
        prev_pos = 0
        positions = [pos for pos, char in enumerate(word_so_far) if char == '-']
        # is first char a hyphen, if so not legal word
        if positions[0] == 0:
            return False
        for pos in positions: #not necessarily working for more than one -
            if pos+1 ==len(word_so_far): #deal with trailing - kick it out for now
                return False
            if word_so_far[pos-1]>word_so_far[pos+1]: # deal with wraparound later W-S is illegal in meantime
                return False
            regex_str = regex_str[0:pos-1] + r'['+ regex_str[pos-1]+r'-' +regex_str[pos+1]+ r']'+regex_str[pos+2:]
            prev_pos = pos
    if '.' in word_so_far:
        pass #  we don't have to do anything to turn . into  legal regex
    regex_str = regex_str.lower()
    return(regex_str)

def can_word_start_like_this(word_so_far):
    '''
    this check should kick out words that can't possibly begin like this
    currently pretty inefficient  , there is prob. some smart way to do this
    we already checked if the word itself is in the dictionary of legal words, so no need to check that
    todo keep list of stuff already checked to avoid checking multiple times
    :param word_so_far:
    :return:
    '''
    if set.intersection(set(REGEX_CHARS),set(word_so_far)):   #
        if len(word_so_far)<3: #avoids hard matching problem, just allow everything for now
            return True
        if word_so_far.rfind('-')==len(word_so_far)-1: # let all trailing hyphens thru
            return True
        regex_str = transform_to_legal_regex(word_so_far)
        if not regex_str:
            return False
        regex_str = r'^' + regex_str
        myregex = re.compile(regex_str)
        for word in LEGAL_WORDS:
            if myregex.match(word):
                return True
        return False
    l = len(word_so_far)
    word_beginnings_of_greater_length = [word[0:l] for word in LEGAL_WORDS if len(word)>l]
    if word_so_far.lower() in word_beginnings_of_greater_length:
        return True
    return False

def board_stats(dies):
    all_results=[]
    with open('board_stats.txt', 'a') as fp:
        fp.write('\nDies')
        for i,die in enumerate(dies):
            fp.write(f'[')
            for s in die:
                fp.write(f'{s},')
            fp.write(f']')
        fp.write('\n')
        while(1):
            board = generate_boggleboard(dies)
            print_board(board)
            fp.write('board:')
            for row in range(4):
                for col in range(4):
                    fp.write(f'{board[row][col]} ')
                fp.write('')
            words = sorted(find_words(board))
            print(f'all words: {words}')

            n_words=len(words)
            all_results.append(n_words)
            avg = np.mean(all_results)
            std = np.std(all_results)
            min = np.min(all_results)
            max = np.max(all_results)
            print(f'n words {n_words} avg {avg:.3} std {std:.3}')
            fp.write(f'\tn_words {n_words} \tavg {avg:.3} \tstd {std:.3} \tmin {min} \tmax {max} \tN {len(all_results)}\twords:{words}')
            fp.write('\n')
            fp.flush()
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

ALTERNATE_DIES = [
        ['.','A','E','E','G','N'],
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


#board_stats(STANDARD_DIES)
board_stats(ALTERNATE_DIES)
#board = generate_boggleboard(STANDARD_DIES)
board = [['R',	'I',	'E',	'L'],
    ['A',	'Qu',	'D',	'E'	],
    ['T'	,'V',	'R',	'P'],
    ['O',	'C',	'I',	'T'	]]
board = [[  'S'	,'S',	'X',	'K'],
    ['D',	'S',	'N',	'T'],
    ['W',	'V',	'G',	'T'],
    ['H',	'A',	'Z',	'W']]
test_hyphen = [[  'S'	,'S',	'X',	'K'],
    ['-',	'S',	'N',	'T'],
    ['W',	'V',	'G',	'T'],
    ['H',	'E',	'Z',	'W']]
test_dot = [['S', 'S', 'X', 'K'],
               ['.', 'S', 'N', 'T'],
               ['W', 'V', 'G', 'T'],
               ['H', 'E', 'Z', 'W']]

# board = test_dot
# print_board(board)
# found_words = find_words(board)
# #print(found_words)
