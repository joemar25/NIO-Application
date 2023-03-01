# John Olan S. Gomez | Joemar
# February 19, 2023 - Update

from gingerit.gingerit import GingerIt as gingerit  # checks grammar
import nltk.data  # separates sentences


class Grammar:

    # Check if the punkt package is already downloaded
    # If it's not downloaded, download it now
    if not nltk.download('punkt', quiet=True):
        nltk.download('punkt')

    # Steps:
    # get the paragraph
    # separate the paragraph into sentences
    # correct the grammar in each sentence
    # recombine the sentences

    def __init__(self, sentence):
        self.sentence = sentence
        self.sentences = []

    def __separateParagraph(self):
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        data = self.sentence
        self.sentences.append(tokenizer.tokenize(data))

    def checkGrammar(self):
        Grammar.__separateParagraph(self)  # separate the sentences
        correctSentence = []    # array to hold the corrected sentences
        parser = gingerit()     # parse gingerit

        # loop through the sentences one by one
        for i in self.sentences:
            for j in i:
                result = parser.parse(j)
                correctSentence.append(result['result'])

        # join the corrected sentences
        complete = " ".join(correctSentence)

        return complete
