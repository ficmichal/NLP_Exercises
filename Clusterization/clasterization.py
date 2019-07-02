import re
import editdistance


def preprocess(address, stoplist):
    address = address.lower()
    address = ''.join(filter(lambda c: not c.isdigit(), address))
    address = handle_stoplist(address, stoplist, '')
    address = re.sub(r'[\w\.-]+@[\w\.-]+', '', address)
    address = address.replace(' ', '')
    address = address.split(',', 1)[0]
    address = address.split('.', 1)[0]
    return address


def handle_stoplist(main_string, stoplist, new_string):
    for elem in stoplist:
        if elem in main_string:
            main_string = main_string.replace(elem, new_string)

    return main_string


stoplist = ['f.h.', 'f.h.u', 'fhu', 'f.p.h', 'firma', 'pt.', 'pt', 'company', 'tel', 'fax', 'phone', 'nip', 'mobile', 'kom',
            'email', 'contact', 'ul', 'str', 'st', 'street', 'al','ulica', 'logistics'
            '"', '?', '!', ':', ';', '[', ']', '(', ')', '–', '-', '%', "'", '+', '/']
original_text_lines = [line.rstrip('\n') for line in open('data/lines.txt', 'r', encoding='utf-8')]
original_text_lines_dict = dict(enumerate(original_text_lines))
preprocessed_dict = {k: preprocess(v, stoplist) for k, v in original_text_lines_dict.items()}
clusters = [[preprocessed_dict[0], 0]]

for i in range(1, len(preprocessed_dict)):
    flag = 0
    norm = 0.3 * len(preprocessed_dict[i])
    for addresses in clusters:
        curr_dis = editdistance.eval(preprocessed_dict[i], addresses[0])
        if curr_dis <= norm:
            flag = 1
            addresses.append(i)
            break
    if flag == 0:
        clusters.insert(0, [preprocessed_dict[i], i])

with open('data/clusteredLev.txt', 'w', encoding='utf-8') as file:
    for addresses in reversed(clusters):
        for i in range(1, len(addresses)):
            file.write(original_text_lines_dict[addresses[i]])
        file.write('##########' + '\n')
