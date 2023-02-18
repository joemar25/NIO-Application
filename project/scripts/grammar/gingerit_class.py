# John Olan S. Gomez
# SE2 Final project
# February 16, 2023

from gingerit.gingerit import GingerIt as gingerit  #checks grammar
import nltk.data    #separates sentences
# nltk.download('punkt')  #you can comment this out, once it is already downloaded

class Grammar:

    # Steps:
    # get the paragraph
    # separate the paragraph into sentences
    # correct the grammar in each sentence
    # recombine the sentences

    def __init__(self, sentence):
        self.sentence = sentence
        self.sentences = []

    def separateParagraph(self):
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        data = self.sentence
        self.sentences.append(tokenizer.tokenize(data))

    def checkGrammar(self):
        Grammar.separateParagraph(self) # separate the sentences
        correctSentence = []    # array to hold the corrected sentences
        parser = gingerit()     # parse gingerit

        # loop through the sentences one by one
        for i in self.sentences:
            for j in i:
                result = parser.parse(j)
                correctSentence.append(result['result'])

        complete = " ".join(correctSentence)    # join the corrected sentences

        return complete
