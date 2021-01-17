import os
import unicodedata

import matplotlib.pyplot as plt


class CommonUtils:
    def strip_accents(self, text):
        choices = {"İ": "I", "ı": "I", "Ş": "S", "Ü": "U", "Ö": "O", "Ç": "C", "Ğ": "G", "i": "i", "ç": "c", "ğ": "g",
                   "ö": "o",
                   "ş": "s", "ü": "u"}
        for i in range(len(text)):
            text = text.replace(text[i:i + 1], choices.get(text[i], text[i]))
        return ''.join(char for char in
                       unicodedata.normalize('NFKD', text)
                       if unicodedata.category(char) != 'Mn')

    def plot_histograms(self, dictionary, colors, title, path):
        plt.bar(list(dictionary.keys()), dictionary.values(), color=colors)
        plt.title(title)
        plt.xlabel("Respective Answers and their counts are attached in excel file")
        plt.savefig(path)
        plt.clf()

    def clean_output_folder(self, folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))