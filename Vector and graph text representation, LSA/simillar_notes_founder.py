from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
from numpy import percentile
from numpy import array
from math import sqrt
from common_functions import *


def found_similiar_notes_by_tfidf(notes):
    norms = {}
    vect = TfidfVectorizer().fit(notes)
    note_to_compare = notes[18]
    similiar_notes = {18: note_to_compare}
    for i in range(len(notes)):
        tfidf = vect.transform([note_to_compare, notes[i]])
        norms[i] = (tfidf * tfidf.T).A[0, 1] # get index of 2x2 matrix

    similiar_notes.update(take_similar_notes_by_upper(norms, is_graph_method=False))
    return list(similiar_notes.keys())


def found_similiar_notes_by_distance_graph(notes, n):
    norms_dice = {}
    notes_words = split_notes(notes)
    note_to_compare = notes_words[18]
    note_to_compare_graph, note_graph_length = graph_distance(note_to_compare, n)
    similiar_notes = [18]
    for i in range(len(notes_words)):
        comparision_note_graph, cmp_note_graph_length = graph_distance(notes_words[i], n)
        norms_dice[i] = calculate_graph_distance(note_to_compare_graph, comparision_note_graph, note_graph_length, cmp_note_graph_length)
        #norms_eucl[i] = calculate_graph_distance_euclides(note_to_compare_graph, comparision_note_graph)

    return similiar_notes + list(take_similar_notes_by_upper(norms_dice))


def calculate_graph_distance(note_graph, comparision_note_graph, note_graph_length, comparision_note_graph_length):
    dice_numerator = 0
    for branched_word in note_graph:
        for word in note_graph[branched_word]:
            if branched_word in comparision_note_graph and word in comparision_note_graph[branched_word]:
                compare_value = comparision_note_graph[branched_word][word]
                original_value = note_graph[branched_word][word]
                if compare_value > original_value:
                    dice_numerator += original_value
                else:
                    dice_numerator += compare_value
    return (2 * dice_numerator) / (note_graph_length + comparision_note_graph_length)


def calculate_graph_distance_euclides(note_graph, comparision_note_graph):
    euclides_vector = []
    for branched_word in note_graph:
        for word in note_graph[branched_word]:
            if branched_word in comparision_note_graph and word in comparision_note_graph[branched_word]:
                euclides_vector.append((note_graph[branched_word][word] - comparision_note_graph[branched_word][word])**2)
            else:
                euclides_vector.append(note_graph[branched_word][word]**2)
    for branched_word in comparision_note_graph:
        for word in comparision_note_graph[branched_word]:
            if branched_word not in note_graph or word not in note_graph[branched_word]:
                euclides_vector.append(comparision_note_graph[branched_word][word]**2)
    return sqrt(sum(euclides_vector))


def graph_distance(words, n):
    vector_length = 0
    graph = defaultdict(lambda: defaultdict(int))
    window_iter = [words[x:x+n] for x in range(len(words))]
    for it in window_iter:
        for i in it:
            graph[it[0]][i] += 1
            vector_length += 1
    return graph, vector_length


def split_notes(notes):
    split_notes = []
    for note in notes:
        split_notes.append(note.split())
    return split_notes


def take_similar_notes_by_upper(calc_norms_dict, is_graph_method=True):
    # calculate interquartile range
    q_percentile = 0; cut_off_coeff = 1
    calc_norms = array(list(calc_norms_dict.values()))
    if is_graph_method:
        q_percentile = 98
        cut_off_coeff = 1.25
    else:
        q_percentile = 99
    q = percentile(calc_norms, q_percentile)
    cut_off = q * cut_off_coeff
    upper = q + cut_off
    # identify outliers
    return {k: v for k, v in calc_norms_dict.items() if v > upper}


def take_similar_notes_by_lower(calc_norms_dict):
    # calculate interquartile range
    calc_norms = array(list(calc_norms_dict.values()))
    q1 = percentile(calc_norms, 1)
    cut_off = q1 * 0.75
    lower = q1 - cut_off
    # identify outliers
    return {k: v for k, v in calc_norms_dict.items() if v < lower}


def save_results(scores):
    with open(f'results/stats.txt', 'w', encoding='utf-8') as file:
        for i in range(len(scores)):
            if i == 0:
                file.write('TFIDF stats:\n')
                file.write(f'''Precision = {scores[i][0].__format__('0.3f')}, Recall = {scores[i][1].__format__(
                    '0.3f')}, F1 = {scores[i][2].__format__('0.3f')}\n\n''')
            else:
                file.write(f'{i}-graph stats:\n')
                file.write(f'''Precision = {scores[i][0].__format__('0.3f')}, Recall = {scores[i][1].__format__(
                    '0.3f')}, F1 = {scores[i][2].__format__('0.3f')}\n\n''')

all_similar_notes = []
notes, original_notes = read_notes(create_basic_polish_form_dict())

similiar_notes_by_tfidf = found_similiar_notes_by_tfidf(notes)
all_similar_notes.append(similiar_notes_by_tfidf)
save_similar_notes(original_notes, similiar_notes_by_tfidf, 'tfidf')

for n in range(1, 7):
    similiar_notes_by_graph = found_similiar_notes_by_distance_graph(notes, n)
    all_similar_notes.append(similiar_notes_by_graph)
    save_similar_notes(original_notes, similiar_notes_by_graph, f'{n}_graph')

save_results(calculate_stats(all_similar_notes))
