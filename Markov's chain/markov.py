import os
import string
import itertools
from collections import Counter, defaultdict


def calc_prob(markov_chain, author, ngram):
    if len(ngram) == 1:
        return 0
    x = ' '.join(ngram[:-1])
    P = zero_divide(markov_chain[author][x][ngram[-1]], markov_chain['all_data'][x]['#sum#'])
    if P != 0:
        return P
    return back_off_weight(markov_chain, author, ngram[:-1])


def back_off_weight(m_chain, author, ngram):
    x = ' '.join(ngram)
    x_ = ' '.join(ngram[:-1])
    bow = zero_divide((1 - zero_divide(m_chain[author][x]['#sum#'], m_chain['all_data'][x]['#sum#'])),
            (1 - zero_divide(m_chain[author][x_]['#sum#'], m_chain['all_data'][x_]['#sum#'])))
    if bow == 0:
        bow = 0.4
    return bow * calc_prob(m_chain, author, ngram[:-1])


def zero_divide(x1, x2):
    if x1 == 0 or x2 == 0:
        return 0
    return x1 / x2


train_path = 'data/train/'
test_path = 'data/test/'
authors = ['AlistairMacLean', 'AndreNorton', 'JacekDukaj', 'WilliamGibson']
transform_table = dict((ord(ch), None) for ch in (string.punctuation + string.digits))
rank = 4
markov_chain = defaultdict(lambda: defaultdict(Counter))

for author in authors:
    path = train_path + author + '/'
    for filename in os.listdir(path):
        lines = [line.rstrip('\n').lower().translate(transform_table).split() for line in
                 open(path + filename, 'r', encoding='utf-8')]
        words = list(itertools.chain.from_iterable(lines))

        for i in range(len(words) - rank):
            ngram = words[i:i + rank]
            for j in range(-1, -rank, -1):
                x = ' '.join(ngram[:j])
                markov_chain[author][x][ngram[j]] += 1
                markov_chain[author][x]['#sum#'] += 1
                markov_chain['all_data'][x][ngram[j]] += 1
                markov_chain['all_data'][x]['#sum#'] += 1

markov_results = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
for org_author in authors:
    path = test_path + org_author + '/'
    for book in os.listdir(path):
        lines = [line.rstrip('\n').lower().translate(transform_table).split() for line in
                 open(path + book, 'r', encoding='utf-8')]
        words = list(itertools.chain.from_iterable(lines))

        for i in range(len(words) - rank):
            ngram = words[i:i + rank]
            for author in authors:
                markov_results[org_author][book][author] += calc_prob(markov_chain, author, ngram)

stats = defaultdict(int)
num_of_authors = len(authors)
for org_author in authors:
    for book in markov_results[org_author]:
        book_results = markov_results[org_author][book]
        if org_author == sorted(book_results, key=book_results.get, reverse=True)[0]:
            stats['tp'] += 1
            stats['tn'] += num_of_authors - 1
        else:
            stats['fp'] += 1
            stats['tn'] += num_of_authors - 2
            stats['fn'] += 1

precision = stats['tp'] / (stats['tp'] + stats['fp'])
recall = stats['tp'] / (stats['tp'] + stats['fn'])