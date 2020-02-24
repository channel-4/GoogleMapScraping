import csv


class WriteCsv:

    def __init__(self, search_word, info):
        self.search_word = search_word
        self.info = info
        self.writeFile()

    def writeFile(self):
        with open('./csv/' + self.search_word + '.csv', 'w') as f:
            writer = csv.writer(f, lineterminator="\n")
            writer.writerows(self.info)
