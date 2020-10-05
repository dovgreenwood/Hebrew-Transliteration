"""
@author Dov Greenwood
@date March 18, 2020
@description Transliterates Hebrew text from a file into English characters, printing the output.
"""

"""DATA STRUCTURES AND FUNCTION DEFINITIONS"""

#The sounds of every letter without a dagesh, including also ending letters.
#Distinct characters are given to each letter, but are changed to their standardized transliteration in the final output.
#Changing from Hebrew letter unicode to English parallels isn't strictly speaking necesary, but makes the program more readable.
letters = {
    0x5D0: 'x',
    0x5D1:'v', 0x5D2:'g', 0x5D3:'d', 0x5D4:'h',
    0x5D5:'w',
    0x5D6:'z', 0x5D7:'ch', 0x5D8:'t', 0x5D9:'y',
    0x5DB:'kh', 0x5DA:'kh',
    0x5DC:'l',
    0x5DE:'m', 0x5DD:'m',
    0x5E0:'n', 0x5DF:'n',
    0x5E1:'s',
    0x5E2:'c',
    0x5E4:'f', 0x5E3:'f',
    0x5E6:'ts', 0x5E5:'ts',
    0x5E7:'q', 0x5E8:'r',
    0x5E9:'sh',
    0x5EA:'t',

    0:''
}

#dagesh and list of transformations
dagesh = 0x5BC
altered = {
    'v':'b', 'w':'u',
    'kh':'k', 'f':'p'
}

#shin/sin extension
shin = {
    0x5C2:'',
    0x5C1:'h'
}

#letter pairs that should separated by an apostraphe to increase clarity
bad_pairs = [['s', 'ch'], ['s', 'kh'], ['t', 'ch'], ['t', 'kh'], ['ts', 'h'], ['s', 'h'], ['sh', 'h']]


#short vowel characters
#kamatz can take on an o or a sound depending on the letter under which it appears
vowels = {
    0x5B7:'a', 0x5B2:'a', 0x5B3:'a',
    0x5B8:'a', #kamatz
    0x5BA:'o', 0x5B9:'o',
    0x5B4:'i',
    0x5B6:'e', 0x5B1:'e',
    0x5B5:'ei',
    0x5BB:'u',
    0x5B0:"'",

    0:''
}


end_characters = {' ', '\n', '\t', ',', '.', ':'}



def last_index(char, chars):
    for i in range(len(chars) - 1, -1, -1):
        if chars[i] == char:
            return i
    return False

def curr_word(chars):
    word = []
    for i in range(len(chars) - 1, -1, -1):
        if chars[i] in end_characters:
            break
        if chars[i] == '':
            continue
        else:
            word.append(chars[i])
    return word[::-1]

def last_letter(word):
    for i in range(len(word) - 1, -1, -1):
        if word[i] in letters.values():
            return word[i]
    return False

def last_vowel(word):
     for i in range(len(word) - 1, -1, -1):
         if word[i] in vowels.values() and word[i]:
             return word[i]
     return False

def shva_na(word):
    if len(word) > 1:
        return False
    return True

def remove_h(word):
    if len(word) <= 1 or word[-1] != 'h':
        return False
    if last_vowel(word) == 'a' or last_vowel(word) == 'ei' or last_vowel(word) == 'o':
        return True
    return False

def move_vowel_back(word):
    lv = last_vowel(word)
    ll = last_letter(word)
    return (lv == 'a') and (ll == 'h' or ll == 'ch') and (last_index(lv, word) > last_index(ll, word))





"""FILE INPUT"""

#made as a map in case more punctuation swaps need to be added
alt_punc = {':':'.', '.':',', '-':' '}

file = input('file: ')
punc = input('replace punctuation? (y/n): ') == 'y'

text = ''
with open(file, 'r', encoding='utf8') as contents:
    text = contents.read()
if alt_punc:
    for i in alt_punc:
        text = text.replace(i, alt_punc[i])
text += ' '





"""TRANSLITERATION PROCESS"""
engl = []

for i in text:
    unic = ord(i)

    if unic in letters.keys():
        if letters[unic] == 'y' and (last_vowel(curr_word(engl)) == 'i' or last_vowel(curr_word(engl)) == 'ei'):
            engl.append('')
        else:
            engl.append(letters[unic])

    elif unic == dagesh:
        if last_letter(curr_word(engl)) in altered.keys():
            engl[last_index(last_letter(curr_word(engl)), engl)] = altered[last_letter(curr_word(engl))]
        engl.append('')

    elif unic in shin:
        engl[last_index('sh', engl)] += shin[unic]
        engl.append('')

    elif unic in vowels.keys():
        if vowels[unic] == "'" and (not shva_na(curr_word(engl))):
            engl.append('')
            continue
                #  kamatz, the common exception for the word kol/khol
        if unic == 0x5B8 and (last_letter(curr_word(engl)) == 'k' or last_letter(curr_word(engl)) == 'kh'):
            engl.append('o')
            continue
        if vowels[unic] == 'o' and last_letter(curr_word(engl)) == 'w':
            engl = engl[:-1]
            engl.append('')
        engl.append(vowels[unic])

    elif i in end_characters:
        if remove_h(curr_word(engl)):
            engl = engl[:-1]
            engl.append('')
        if move_vowel_back(curr_word(engl)):
            temp = engl[-1]
            engl[-1] = engl[-2]
            engl[-2] = temp
        engl.append(i)

    else:
        engl.append('')

output = ''
last = ''
for i in engl:
    #skip silent letters, alef and ayin
    if i == 'x' or i == 'c' or i == '':
        continue

    if [last, i] in bad_pairs:
        output += "'"
    if last == i and (not i in end_characters) and (not i == ''):
        output += "'"

    if i == 'w':
        output += 'v'
    elif i == 'kh':
        output += 'ch'
    elif i == 'q':
        output += 'k'
    elif i == 'sh':
        output += 's'
    elif i == 'shh':
        output += 'sh'
    else:
        output += i

    last = i

print(output)
