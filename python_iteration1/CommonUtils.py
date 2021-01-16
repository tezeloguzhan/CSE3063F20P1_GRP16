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