import re
from collections import defaultdict


class Preprocess:
    def __init__(self, original_filename):
        self.original_filename = original_filename

    def preprocess(self):
        all_words_dict = defaultdict(int)
        self.original_text_lines = [line.rstrip('\n') for line in open(f'data/{self.original_filename}.txt',
                                                                  'r', encoding='utf-8')]
        self.original_text_lines_dict = dict(enumerate(self.original_text_lines))
        self.preprocessed_dict = {k: self.__preprocess_raw(v, self.basicStoplist, all_words_dict) for k, v in
                                  self.original_text_lines_dict.items()}
        all_words = sorted(all_words_dict.items(), key=lambda kv: kv[1], reverse=True)
        hybrid_stoplist = [w[0] for w in all_words if w[1] > 110 and w[0] != 'ooo' and w[0] != 'order']
        self.preprocessed_dict = {k: self.__handle_stoplist(v, hybrid_stoplist, '') for k, v in
                                  self.preprocessed_dict.items()}

    def __preprocess_raw(self, address, stoplist, all_words_dict):
        address = address.lower()
        preprocessed_address = ''.join(filter(lambda c: not c.isdigit(), address))
        preprocessed_address = self.__handle_stoplist(preprocessed_address, stoplist, '')
        preprocessed_address = re.sub(r'[\w\.-]+@[\w\.-]+', '', preprocessed_address)
        preprocessed_address = ' '.join(preprocessed_address.split())
        words = preprocessed_address.split()
        for word in words:
            all_words_dict[word] += 1
        preprocessed_address = preprocessed_address.replace(' ', '')
        return preprocessed_address

    @staticmethod
    def __handle_stoplist(main_string, stoplist, new_string):
        for elem in stoplist:
            if elem in main_string:
                main_string = main_string.replace(elem, new_string)
        return main_string

    basicStoplist = ['f.h.', 'f.h.u', 'fhu', 'f.p.h', 'firma', 'pt.', 'pt', 'company', 'tel', 'fax', 'phone', 'nip',
                     'mobile', 'kom', 'pte', 'ltd', 's.a', 'sa',
                     'email', 'contact', 'ul', 'str', 'st', 'street', 'al', 'ulica', 'logistics',
                     '.', ',', '"', '?', '!', ':', ';', '[', ']', '(', ')', '–', '-', '%', "'", '+', '/', '<', '>']
