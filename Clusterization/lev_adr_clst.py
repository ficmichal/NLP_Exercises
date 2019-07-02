import editdistance
import adr_clst
import numpy as np
from weighted_levenshtein import lev

class LevenstheinClusterization(adr_clst.AddressClusterization):
    def __init__(self, original_filename):
        super().__init__('Levensthein', original_filename)

    def cluster_data(self):
        clusters = [[self.clustered_data[0][0]]]
        for i in range(1, len(self.preprocessed_dict)):
            print(i)
            flag = 0
            norm = 0.3 * len(self.preprocessed_dict[i])
            for adr in range(0, len(self.clustered_data)):
                best_curr_norm = min([self.distance(self.preprocessed_dict[i], x) for x in clusters[adr]])
                if best_curr_norm <= norm:
                    flag = 1
                    self.clustered_data[adr].append(i)
                    clusters[adr].append(self.preprocessed_dict[i])
                    break
            if flag == 0:
                self.clustered_data.insert(0, [self.preprocessed_dict[i], i])
                clusters.insert(0, [self.preprocessed_dict[i]])

    def distance(self, s0, s1):
        if s0 == s1:
            return 0.0
        if len(s0) == 0:
            return len(s1)
        if len(s1) == 0:
            return len(s1)

        v0 = [0] * (len(s1) + 1)
        v1 = [0] * (len(s1) + 1)

        for i in range(len(v0)):
            v0[i] = i

        for i in range(len(s0)):
            v1[0] = i + 1
            for j in range(len(s1)):
                cost = 1
                if s0[i] == s1[j]:
                    cost = 0
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            v0, v1 = v1, v0

        return v0[len(s1)]