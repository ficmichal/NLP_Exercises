import matplotlib.pylab as plt
from collections import defaultdict
from scipy.optimize import curve_fit
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

def zipf_func(x, k):
    return k / x


def mandelbrot_func(x, P, d, B):
    return P / ((x + d)**B)


def replace_invalid_chars(main_string, to_be_replaces, new_string):
    for elem in to_be_replaces:
        if elem in main_string:
            main_string = main_string.replace(elem, new_string)

    return main_string


def create_ngram(data, n):
    result = defaultdict(int)
    for word in data:
        for j in range(len(word) - n + 1):
            ngram = word[j:j + n]
            result[ngram] += 1
    return result


def create_dictionary_of_all_words(char_to_be_replaced):
    dict_of_words = {}
    with open('data/potop.txt', 'r', encoding='utf-8') as file:
        data = file.read().lower().replace('\n', ' ')
        data = replace_invalid_chars(data, char_to_be_replaced, '')
        data = ''.join(filter(lambda c: not c.isdigit(), data))
        data = ' '.join(data.split())
        text_words = data.split()
    lines = [line.rstrip('\n') for line in open('data/odm.txt', 'r', encoding='utf-8') if
             line.count(' ') == line.count(',')]
    clean_lines = [x.lower().replace(',', '').split() for x in lines]

    for line in clean_lines:
        for word in line:
            dict_of_words[word] = line[0]
    return text_words, dict_of_words, data


def create_ranking(text_words, dict_of_words):
    ranking = defaultdict(int)
    for word in text_words:
        if word in dict_of_words:
            ranking[dict_of_words[word]] += 1
    return sorted(ranking.items(), key=lambda kv: kv[1], reverse=True)


def comparision_plot(ranking):
    y_data = [x[1] for x in ranking if x[1] > 600]
    x_data = [x[0] for x in ranking[0:len(y_data)]]
    x_numeric_data = [x for x in range(1, len(x_data) + 1)]

    p1, _ = curve_fit(zipf_func, x_numeric_data, y_data, p0=[18000])
    p2, _ = curve_fit(mandelbrot_func, x_numeric_data, y_data, p0=[4, 4, 4])

    plt.plot(x_data, zipf_func(x_numeric_data, *p1), label='Zipf function')
    plt.plot(x_data, mandelbrot_func(x_numeric_data, *p2), label='Mandelbrot function')
    plt.step(x_data, y_data, label='Occurrence in text')
    plt.xticks(fontsize=6, rotation='vertical')
    plt.legend()
    plt.show()
    return p1, p2


def count_hapax_logomena(ranking):
    return len([x[1] for x in ranking if x[1] == 1])


def count_fifty_percent_of_text(ranking, text_words):
    sum_of_words = 0
    i = 0
    fifty_percent_of_text = 0
    while sum_of_words <= len(text_words) / 2:
        sum_of_words += ranking[i][1]
        i += 1
        fifty_percent_of_text += 1
    return fifty_percent_of_text


def extend_zipf_plot(ranking, text_words, fifty_percent_of_text):
    y_data = list(np.cumsum([ranking[i][1] * 100 / len(text_words) for i in range(0, fifty_percent_of_text)]))
    x_data = [x[0] for x in ranking[0:len(y_data)]]
    plt.plot(x_data, y_data)
    plt.xticks(fontsize=5, rotation='vertical')
    plt.show()


def save_results(ranking, hapax_legomena, fifty_percent_of_text, p1, p2):
    with open('results/ranking.txt', 'w', encoding='utf-8') as file:
        for k, v in ranking:
            file.write(str(k) + ' : ' + str(v) + '\n')
    with open(f'results/main_stats.txt', 'w', encoding='utf-8') as file:
        file.write(
            f'Count of hapax legomena: {hapax_legomena}.\nCount of words, which contains 50% of text: {fifty_percent_of_text}.')
        file.write(f'K: {p1}.\nP: {p2[0]} d: {p2[1]} B: {p2[2]}.')


def crete_ngram_statistics(isBase, text_words):
    ext = 'base' if isBase else ''
    for n in range(2, 4):
        ngram_dict = create_ngram(text_words, n)
        with open(f'results/{n}-gram_{ext}stats.txt', 'w', encoding='utf-8') as file:
            for k, v in sorted(ngram_dict.items(), key=lambda kv: kv[1], reverse=True):
                file.write(str(k) + ' : ' + str(v) + '\n')


def crete_word_ngram_statistics(data, n):
    cv = CountVectorizer(ngram_range=(n, n), analyzer='word')
    ranking = cv.fit_transform([data])
    names = cv.get_feature_names()
    counts = ranking.sum(axis=0).A1
    return dict(zip(names, counts))


def save_ngram_results(data, n):
        with open(f'results/{n}-gram_word_stats.txt', 'w', encoding='utf-8') as file:
            for k, v in sorted(data.items(), key=lambda kv: kv[1], reverse=True):
                file.write(str(k) + ' : ' + str(v) + '\n')