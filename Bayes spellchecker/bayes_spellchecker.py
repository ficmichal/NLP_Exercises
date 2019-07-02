from collections import defaultdict
from weighted_levenshtein import lev
import numpy as np


def handle_polish_word(polish_chars_dict, word):
    for i in range(len(word)):
        if word[i] in polish_chars_dict:
            word = word.replace(word[i], polish_chars_dict[word[i]])
    return word


def replace_invalid_chars(main_string, to_be_replaces, new_string):
    for elem in to_be_replaces:
        if elem in main_string:
            main_string = main_string.replace(elem, new_string)
    return main_string


def init_weighted_lev_dicts():
    substitute_costs = np.ones((128, 128), dtype=np.float64)
    insert_costs = np.ones(128, dtype=np.float64)
    delete_costs = np.ones(128, dtype=np.float64)

    substitute_costs[ord('a'), ord('A')] = 0.001  # ą
    substitute_costs[ord('c'), ord('C')] = 0.001  # ć
    substitute_costs[ord('e'), ord('E')] = 0.001  # ę
    substitute_costs[ord('l'), ord('L')] = 0.001  # ł
    substitute_costs[ord('o'), ord('O')] = 0.001  # ó
    substitute_costs[ord('n'), ord('N')] = 0.001  # ń
    substitute_costs[ord('s'), ord('S')] = 0.001  # ś
    substitute_costs[ord('z'), ord('X')] = 0.001  # ź
    substitute_costs[ord('z'), ord('Z')] = 0.001  # ż

    substitute_costs[ord('O'), ord('u')] = 0.01  # ó -> u
    substitute_costs[ord('u'), ord('O')] = 0.01  # u -> ó
    substitute_costs[ord('r'), ord('s')] = 0.1  # rz -> sz
    substitute_costs[ord('s'), ord('r')] = 0.1  # sz -> rz
    insert_costs[ord('r')] = 0.1  # ż -> rz
    substitute_costs[ord('Z'), ord('z')] = 0.001
    delete_costs[ord('r')] = 0.1  # rz -> ż
    insert_costs[ord('c')] = 0.1  # h -> ch
    delete_costs[ord('c')] = 0.1  # ch -> h
    substitute_costs[ord('p'), ord('b')] = 0.8  # p -> b
    substitute_costs[ord('j'), ord('i')] = 0.75  # j -> i
    substitute_costs[ord('t'), ord('d')] = 0.9  # t -> d

    return insert_costs, delete_costs, substitute_costs


def find_by_first_chars(wrong_word, polish_mistakes_dict):
    if len(wrong_word) < 2:
        return wrong_word
    first_chars_of_wrong_word = wrong_word[0]
    all_possibilites = [first_chars_of_wrong_word]
    for c in first_chars_of_wrong_word:
        if c in polish_mistakes_dict:
            for dict_c in polish_mistakes_dict[c]:
                all_possibilites.append(dict_c)
    return tuple(all_possibilites)


def bayes(wrong_word, words_dict, polish_chars_dict):
    insert_costs, delete_costs, substitute_costs = init_weighted_lev_dicts()
    polish_mistakes_dict = {'r': ['Z', 's'], 'c': ['h'], 'z': ['Z', 'X', 'r'], 'n': ['ń'], 's': ['S'], 'l': ['L'],
                            'o': ['O', 'u'], 'u': ['O'], 'h': ['c']}
    Pwc_dict = {cnd: lev(wrong_word, cnd, insert_costs=insert_costs,
                         delete_costs=delete_costs, substitute_costs=substitute_costs) for cnd in words_dict
                if cnd.startswith(find_by_first_chars(wrong_word, polish_mistakes_dict))}
    top_rated = sorted(Pwc_dict.items(), key=lambda kv: kv[1])[:200]
    top_rated_words = [x[0] for x in top_rated]
    top_rated_words_max = max(top_rated, key=lambda v: v[1])[1]
    Pwc = [(x[0], 1 - x[1] / top_rated_words_max) for x in top_rated]  # P(w|c)

    occurences_in_dict = [(x, words_dict[x] + 1) for x in top_rated_words]
    occurences_in_dict_max = max(occurences_in_dict, key=lambda v: v[1])[1]
    Pc = [(x[0], x[1] / occurences_in_dict_max) for x in occurences_in_dict]  # P(c)
    Pcw = []
    for p in range(len(Pwc)):
        Pcw.append((handle_polish_word({v: k for k, v in polish_chars_dict.items()}, Pwc[p][0]),
                    0.8 * Pwc[p][1] + 0.2 * Pc[p][1]))  # P(c|w)
    return [x[0] for x in sorted(Pcw, key=lambda v: v[1], reverse=True)[:5]]

dict_of_words = defaultdict(int)
polish_chars_dict = {'ą': 'A', 'ć': 'C', 'ę': 'E', 'ł': 'L', 'ó': 'O', 'ń': 'N', 'ś': 'S', 'ź': 'X', 'ż': 'Z'}

words = [line.rstrip('\n') for line in open('data/formy.txt', 'r', encoding='utf-8') if 'ú' not in line]
for word in words:
    word = handle_polish_word(polish_chars_dict, word)
    dict_of_words[word] += 1

char_to_be_replaced = ['"', ',', '.', '?', '!', ':', ';', '[', ']', '(', ')', '–', '-', '%', '*', '`', 'ú']
polish_texts = ['dramat', 'popul', 'proza', 'publ', 'wp']
for text in polish_texts:
    with open(f'data/{text}.txt', 'r', encoding='utf-8') as file:
        data = file.read().lower().replace('\n', ' ')
    data = replace_invalid_chars(data, char_to_be_replaced, '')
    data = ''.join(filter(lambda c: not c.isdigit(), data))
    data = ' '.join(data.split())
    text_words = data.split()
    for word in text_words:
        word = handle_polish_word(polish_chars_dict, word)
        dict_of_words[word] += 1

word = input('Write single word:\n')
while word != 'xyz':
    fix_word = handle_polish_word(polish_chars_dict, word)
    if fix_word in dict_of_words:
        print(f'Word {word} exists in polish language.\n\n')
    else:
        hints = bayes(f'{fix_word}', dict_of_words, polish_chars_dict)
        print(f'Word {fix_word} not exists in polish language.\n')
        print(f'I think you mean: {hints[0]}\n')
        print(f'Other possibilites: {hints[1:5]}\n')
    word = input(f"Write another word or write 'xyz' to exit.\n")
