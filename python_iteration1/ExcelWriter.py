import pandas


class ExcelWriter:
    def init(self, dictionary, path):
        self.dictionary = dictionary
        self.path = path

    def write_excel(self):
        df = pandas.DataFrame.from_dict(
            self.dictionary)
        df.to_excel(self.path, header=True, index=False)

    def set_dict(self, new_dict):
        self.dictionary = new_dict

    def set_path(self, new_path):
        self.path = new_path