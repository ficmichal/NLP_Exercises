import statistics as stats


class StatsCalculator:
    def __init__(self, original_text_lines_dict):
        self.original_text_lines_dict = original_text_lines_dict

    def create_clusters(self, data_to_cluster):
        i = 0
        clustered_data = [[]]
        while i < len(data_to_cluster):
            while data_to_cluster[i] != '##########':
                clustered_data[-1].append(data_to_cluster[i])
                i += 1
            clustered_data.append([])
            i += 1
        return clustered_data

    def clusters_to_numbers(self, data, dict_data):
        numeric_data = []
        dict_items = dict_data.items()
        for cluster in data:
            numeric_data.append([])
            for adr in cluster:
                for k, v in dict_items:
                    if v == adr:
                        numeric_data[-1].append(k)
                        break
        return numeric_data

    def calculate_coeffs(self, data_clusters, learn_clusters):
        coeffs = []
        for lc in learn_clusters:
            for dc in range(0, len(data_clusters)):
                cluster_coeffs = [0, 0, 0]  # TP, FP, FN
                if lc[0] in data_clusters[dc]:  # match clusters
                    for i in data_clusters[dc]:
                        if i in lc:
                            cluster_coeffs[0] += 1  # TP
                        else:
                            cluster_coeffs[2] += 1  # FN
                    for j in lc:
                        if j not in data_clusters[dc]:
                            cluster_coeffs[1] += 1  # FP
                    coeffs.append(cluster_coeffs)
                    break
        return coeffs

    def calculate_averages(self, coeffs):
        micro_avg_prec = sum(list(zip(*coeffs))[0]) / (sum(list(zip(*coeffs))[0]) + sum(list(zip(*coeffs))[1]))
        micro_avg_rcll = sum(list(zip(*coeffs))[0]) / (sum(list(zip(*coeffs))[0]) + sum(list(zip(*coeffs))[2]))
        micro_f1 = stats.harmonic_mean([micro_avg_prec, micro_avg_rcll])
        macro_avg_prec = stats.mean([cf[0] / (cf[0] + cf[1]) for cf in coeffs])
        macro_avg_rcll = stats.mean([cf[0] / (cf[0] + cf[2]) for cf in coeffs])
        macro_f1 = stats.harmonic_mean([macro_avg_prec, macro_avg_rcll])

        return micro_avg_prec, micro_avg_rcll, micro_f1, macro_avg_prec, macro_avg_rcll, macro_f1

    def print_result(self, cluster_methods):
        result_text = ''
        learned_clusters = []
        for method in cluster_methods:
            learn_data = [line.rstrip('\n') for line in
                          open(f'results/clustered{method}.txt', 'r', encoding='utf-8')]
            learn_grouped_companies = self.clusters_to_numbers(self.create_clusters(learn_data), self.original_text_lines_dict)
            del learn_grouped_companies[-1]
            learned_clusters.append(learn_grouped_companies)

        data = [line.rstrip('\n') for line in open('data/clusters.txt', 'r', encoding='utf-8') if line != '\n']
        grouped_companies = self.clusters_to_numbers(self.create_clusters(data), self.original_text_lines_dict)
        del grouped_companies[-1]

        for i in range(0, len(learned_clusters)):
            stats = self.calculate_averages(self.calculate_coeffs(grouped_companies, learned_clusters[i]))
            result_text += f"Comparision between 'clusters.txt' and cluster by: {cluster_methods[i]} method.\n"
            result_text += self.print_stats(stats)
            result_text += '\n'

        for i in range(1, len(learned_clusters)):
            stats = self.calculate_averages(self.calculate_coeffs(learned_clusters[0], learned_clusters[i]))
            result_text += f"Comparision between {cluster_methods[0]} and cluster by: {cluster_methods[i]} method.\n"
            result_text += self.print_stats(stats)
            result_text += '\n'

        with open(f'results/stats.txt', 'w', encoding='utf-8') as file:
            file.write(result_text)

    def print_stats(self, stats):
        return f"Micro-average-precision: {stats[0].__format__('0.3f')}\n" \
              + f"Micro-average-recall: {stats[1].__format__('0.3f')}\n"\
              + f"Micro-average-f1: {stats[2].__format__('0.3f')}\n"\
              + f"Macro-average-precision: {stats[3].__format__('0.3f')}\n"\
              + f"Macro-average-recall: {stats[4].__format__('0.3f')}\n"\
              + f"Macro-average-f1: {stats[5].__format__('0.3f')}\n"
