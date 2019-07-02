import abc

class AddressClusterization:
    def __init__(self, clstr_name, preprocessed_data):
        self.clstr_name = clstr_name
        self.preprocessed_dict = preprocessed_data.preprocessed_dict
        self.clustered_data = [[self.preprocessed_dict[0], 0]]
        self.__original_text_lines_dict = preprocessed_data.original_text_lines_dict

    @abc.abstractmethod
    def cluster_data(self):
        return self.clustered_data

    def save_results(self):
        with open(f'results/clustered{self.clstr_name}.txt', 'w', encoding='utf-8') as file:
            for addresses in reversed(self.clustered_data):
                for i in range(1, len(addresses)):
                    file.write(self.__original_text_lines_dict[addresses[i]] + '\n')
                file.write('##########' + '\n')
