from common_functions import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from numpy import asarray, asmatrix, argsort


def found_similiar_notes_by_lsa(notes, idx_note_to_compare, top_similiar):
    tfidf = TfidfVectorizer().fit_transform(notes)
    lsa = TruncatedSVD(n_components=500).fit_transform(tfidf)
    m_lsa = asmatrix(lsa)
    return argsort(asarray(m_lsa[idx_note_to_compare] * m_lsa.T)[0])[::-1][:top_similiar]


def save_results(scores):
    with open(f'results/lsa_stats.txt', 'w', encoding='utf-8') as file:
        file.write('LSA stats:\n')
        file.write(f'''Precision = {scores[0].__format__('0.3f')}, Recall = {scores[1].__format__(
            '0.3f')}, F1 = {scores[2].__format__('0.3f')}\n\n''')


notes, original_notes = read_notes(create_basic_polish_form_dict())
similiar_notes_by_lsa = found_similiar_notes_by_lsa(notes, 18, 400)
save_similar_notes(original_notes, similiar_notes_by_lsa, 'lsa')
save_results(calculate_stats([similiar_notes_by_lsa])[0])
