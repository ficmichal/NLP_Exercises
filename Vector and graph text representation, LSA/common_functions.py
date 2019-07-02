import string
from collections import Counter


def read_notes(basic_form_dict):
    transform_table = dict((ord(ch), None) for ch in (string.punctuation + string.digits))
    notes = []
    original_notes = []
    tmp_note = ''
    notes_lines = [line.rstrip('\n') for line in open('data/pap.txt', 'r', encoding='utf-8')]
    for line in notes_lines[1:]:
        if line[0] == '#':
            original_notes.append(tmp_note)
            tmp_note = to_basic_form(tmp_note.lower().translate(transform_table), basic_form_dict)
            notes.append(tmp_note)
            tmp_note = ''
        else:
            tmp_note = tmp_note + ' ' + line
    original_notes.append(tmp_note)
    tmp_note = to_basic_form(tmp_note.lower().translate(transform_table), basic_form_dict)
    notes.append(tmp_note)

    counter = Counter()
    for line in notes:
        words = line.split()
        for word in words:
            counter[word] += 1
    hapax_legomena = [(k, v) for k, v in counter.items() if v == 1]
    stoplist = dict(counter.most_common(100) + hapax_legomena)

    return handle_stoplist(stoplist, notes), original_notes


def to_basic_form(text, basic_form_dict):
    words = text.split()
    for i in range(len(words)):
        if words[i] in basic_form_dict:
            words[i] = basic_form_dict[words[i]]
    return ' '.join(words)


def create_basic_polish_form_dict():
    dict_of_words = {}
    lines = [line.rstrip('\n') for line in open('data/odm.txt', 'r', encoding='utf-8') if
             line.count(' ') == line.count(',')]
    clean_lines = [x.lower().replace(',', '').split() for x in lines]
    for line in clean_lines:
        for word in line:
            dict_of_words[word] = line[0]
    return dict_of_words


def handle_stoplist(stoplist, notes):
    handled_notes = []
    for note in notes:
        note_words = note.split()
        for i in range(len(note_words)):
            if note_words[i] in stoplist:
                note_words[i] = ''
        handled_note = ' '.join(note_words)
        handled_note = ' '.join(handled_note.split())
        handled_notes.append(handled_note)
    return handled_notes


def calculate_stats(all_similar_notes):
    true_similar_notes = [18, 193, 676, 732, 796, 797, 982, 2372, 2510, 2592, 2794, 3246, 3327, 3453, 3465, 3584, 3601,
                          4040, 4051, 5059, 5105, 5211, 5239, 5251, 5709, 5719, 6062, 6441, 6693, 6739, 7014, 7015,
                          7160, 7338, 7926, 8736, 9404, 9483, 9805, 9806, 9807, 9905, 9989, 10198, 10627, 10831, 10946,
                          11713, 11805, 11964, 12332
                          , 12432, 12735, 12475,
                          12967, 13161, 13354,
13821, 13822, 16026, 16362, 16363, 16766,
17050, 17685, 17846, 18444, 19293, 19315, 19701, 20212, 20556, 20729, 20862, 20863, 20899, 20958, 21194, 21398, 21533,
21544, 22000, 22185, 22238, 22402, 22538, 22614, 22615, 22825, 22945, 23056, 23131, 23181, 23343, 23483, 23623, 24718,
                          24383, 24773, 24850, 24988,
25632, 25903, 26000, 26266, 26280, 26469, 26695, 26906, 27115, 27345, 27546, 27736, 27652, 27947, 28292, 28367, 28959,
                          30166, 30623, 30657, 30898, 30928, 31302, 31630,
31534, 31569, 31630, 31743, 31906, 32174, 32259, 32863, 32864, 33208, 33476, 33546, 34183, 34242, 34948, 35007, 35151,
                          36565, 36711, 36836, 37890,
38230, 38542, 38810, 38839, 38912, 39014, 39262,
39264, 39781, 39782, 40215, 40216, 40343, 40479, 40510, 40607, 40920, 41117, 41440, 41654, 41779, 42142, 42144, 42570,
                          42743, 42848, 43731, 43876, 44297, 44403,
44103, 44404, 44405, 44406, 44742, 45482, 46049, 46050, 46216, 46404, 46617, 47105, 47491, 47552, 48762, 49376, 50743,
                          51475, 51518]
    scores = []
    tp = 0
    fp = 0
    fn = 0
    for similar_notes in all_similar_notes:
        for note in similar_notes:
            if note in true_similar_notes:
                tp += 1
                continue
            if note not in true_similar_notes:
                fp += 1
                continue
        for note in true_similar_notes:
            if note not in similar_notes:
                fn += 1
                continue
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1 = 2 * (precision * recall) / (precision + recall)
        scores.append((precision,
                       recall,
                       f1))
    return scores


def save_similar_notes(original_notes, similiar_notes, method_name):
    with open(f'results/{method_name}.txt', 'w', encoding='utf-8') as file:
        for index in similiar_notes:
            file.write(str(index) + ' ' + original_notes[index] + '\n\n')