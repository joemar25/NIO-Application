from gingerit.gingerit import GingerIt as gingerit  # checks grammar
import nltk.data  # separates sentences
import difflib

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

def grammar_score(input_text, correct_text):
    if input_text == correct_text:
        return 100.0
    text_words = set(input_text.split())
    correct_words = set(correct_text.split())
    common_words = text_words & correct_words
    incorrect_words = text_words - common_words
    seq = difflib.SequenceMatcher(None, input_text, correct_text)
    similarity = seq.ratio()
    score = max((similarity * 100.0) - (len(incorrect_words) * 100.0 / len(text_words)), 0.0)
    return score