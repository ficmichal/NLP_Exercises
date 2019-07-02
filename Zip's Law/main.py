import ranking as r


char_to_be_replaced = ['"', ',', '.', '?', '!', ':', ';', '[', ']', '(', ')', '–', '-', '%']
text_words, dict_of_words, data = r.create_dictionary_of_all_words(char_to_be_replaced)

ranking = r.create_ranking(text_words, dict_of_words)

hapax_legomena = r.count_hapax_logomena(ranking)
fifty_percent_of_text = r.count_fifty_percent_of_text(ranking, text_words)

p1, p2 = r.comparision_plot(ranking)
r.extend_zipf_plot(ranking, text_words, fifty_percent_of_text)

r.save_results(ranking, hapax_legomena, fifty_percent_of_text, p1, p2)
for n in range(2, 4):
    r.save_ngram_results(r.crete_word_ngram_statistics(data, n), n)
