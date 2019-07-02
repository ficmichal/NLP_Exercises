from collections import defaultdict
import adr_clst


class DiceAddressClusterization(adr_clst.AddressClusterization):
    def __init__(self, original_filename):
        super().__init__('DiceCoefficient', original_filename)

    def cluster_data(self):
        norm = 0.4
        n = 3
        clustered_ngrams = [[self.__create_ngram(self.clustered_data[0][0], n)]]
        for i in range(1, len(self.preprocessed_dict)):
            flag = 0
            preprocess_ngram = self.__create_ngram(self.preprocessed_dict[i], n)
            for adr in range(0, len(self.clustered_data)):
                best_curr_norm = min([self.__calc_dice_norm(preprocess_ngram, x) for x in clustered_ngrams[adr]])
                if best_curr_norm <= norm:
                    flag = 1
                    self.clustered_data[adr].append(i)
                    clustered_ngrams[adr].append(preprocess_ngram)
                    break
            if flag == 0:
                self.clustered_data.insert(0, [self.preprocessed_dict[i], i])
                clustered_ngrams.insert(0, [preprocess_ngram])

    def __calc_dice_norm(self, x_ngrams, y_ngrams):
        common_ngrams = 0
        sum_ngrams = sum(x_ngrams.values()) + sum(y_ngrams.values())
        if sum_ngrams == 0:
            return 1
        for key in set(y_ngrams).intersection(set(x_ngrams)):
            if key in x_ngrams:
                if y_ngrams[key] > x_ngrams[key]:
                    common_ngrams += x_ngrams[key]
                else:
                    common_ngrams += y_ngrams[key]
        return 1 - ((2 * common_ngrams) / sum_ngrams)

    def __create_ngram(self, sentence, n):
        result = defaultdict(int)
        for j in range(len(sentence) - n + 1):
            ngram = sentence[j:j + n]
            result[ngram] += 1
        return result
