"""
Grammar class that uses a transformer-based sequence-to-sequence language model to correct grammar errors in text.
This class is initialized with a pre-trained grammar error correction model and provides a method `correct()` to 
correct grammar errors in text. It also provides a method `grammar_score()` to calculate a grammar score between 
an input text and its corrected version.

Attributes:
    sent_detector (nltk.tokenize.punkt.PunktSentenceTokenizer): An instance of the PunktSentenceTokenizer class 
        from the Natural Language Toolkit (nltk) used to split text into sentences.
    correction_tokenizer (transformers.AutoTokenizer): A transformer-based tokenizer instance used to encode input 
        sentences for grammar error correction.
    correction_model (transformers.AutoModelForSeq2SeqLM): A transformer-based sequence-to-sequence language model 
        instance used to correct grammar errors in input sentences.
    device (str): A string indicating the device on which the correction model is run. The default value is "cpu".

Methods:
    __init__(self): Initializes an instance of the Grammar class with a pre-trained grammar error correction model.
    corrector(self, input_sentence, max_candidates=1): Takes an input sentence and returns the corrected version 
        of the sentence using the pre-trained grammar error correction model.
    correct(self, sentences): Takes a string of sentences and returns the corrected version of the sentences by 
        correcting grammar errors using the `corrector()` method. This method also removes extra and duplicate 
        punctuation from the corrected sentences and adds a dot at the end of the sentence if it doesn't already 
        have any punctuation.
    grammar_score(input_text, correct_text): Takes two strings - an input text and its corrected version - and 
        returns a grammar score that represents the similarity between the input text and the corrected text.
"""

import nltk, difflib, re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

if not nltk.download('punkt', quiet=True):
  nltk.download('punkt')

class Grammar:
  
  def __init__(self):
    """
    Initializes an instance of the Grammar class.

    This method loads a pre-trained grammar correction model, sets the device for running the model, and loads the
    sentence tokenizer for English language. If the model is not loaded successfully, an exception is raised.
    """
    
    # Pre-trained model and device configuration
    correction_model_tag = "prithivida/grammar_error_correcter_v1"
    device = "cpu"

    # Load sentence tokenizer and set device
    self.sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    self.device = device
    self.model_loaded = False

    # Load pre-trained grammar correction model and set model_loaded to True if successful
    try:
      self.correction_tokenizer = AutoTokenizer.from_pretrained(correction_model_tag, use_auth_token=False)
      self.correction_model     = AutoModelForSeq2SeqLM.from_pretrained(correction_model_tag, use_auth_token=False)
      self.correction_model     = self.correction_model.to(device)
      self.model_loaded = True
    except Exception as e:
      ...
    """
    If the pre-trained grammar correction model cannot be loaded, an exception is raised and the model_loaded flag
    remains False. This flag can be checked before calling the corrector method to ensure the model is loaded
    successfully.
    """

  def corrector(self, input_sentence, max_candidates=1):
    """
    Applies the grammar correction model to the input sentence and returns the corrected sentence.

    Args:
        input_sentence (str): The sentence to be corrected.
        max_candidates (int, optional): The maximum number of candidate sentences to be generated by the correction
                                        model. Defaults to 1.

    Returns:
        str: The corrected sentence generated by the grammar correction model.
    """
    if not self.model_loaded:
        print("Model is not loaded")  
        return None
    
    input_ids = self.correction_tokenizer.encode("gec: " + input_sentence, return_tensors='pt').to(self.device)
    
    preds = self.correction_model.generate(
        input_ids,
        do_sample=True, 
        max_length=128, 
        num_beams=7,
        early_stopping=True,
        num_return_sequences=max_candidates
    )

    corrected = set(self.correction_tokenizer.decode(pred, skip_special_tokens=True).strip() for pred in preds)
    return list(corrected)[0]
    
  def correct(self, sentences):
    """
    Corrects grammar errors in the input sentences using a pre-trained model and returns the corrected sentences.
    
    Args:
    - sentences: A string containing one or more sentences separated by periods.
    
    Returns:
    A string containing the corrected sentences separated by periods.
    """
    
    # Create a cache to store already corrected sentences
    cache = {}
    
    # Split the input text into individual sentences
    result = []
    for sentence in sentences.split('.'):
        sentence = sentence.strip()
        if sentence:
            # Check if the sentence is already corrected and stored in cache
            if sentence in cache:
                corrected = cache[sentence]
            else:
                # Use the corrector method to correct the sentence
                corrected = self.corrector(sentence)
                cache[sentence] = corrected

            # Remove extra and duplicate punctuation from the corrected sentence
            remove_extra = re.sub(r'[^\w\s]+', lambda m: m.group(0)[0], corrected).rstrip('.')
            
            # Add a dot to the end of the sentence if it doesn't already have any punctuation
            if not remove_extra.endswith((".", "!", "?")):
              remove_extra += "."

            result.append(remove_extra)
            
    # Join the corrected sentences into a single string
    corrected_sentence = ' '.join(result)
    return corrected_sentence
    
def grammar_score(input_text, correct_text):
    """
    Computes the grammar score between the input text and the correct text.

    Args:
    input_text (str): The input text to be scored.
    correct_text (str): The correct text against which the input text will be compared.

    Returns:
    float: The grammar score between the two texts, as a percentage.

    Raises:
    None

    """
    # If the input text matches the correct text exactly, return a perfect score of 100
    if input_text == correct_text:
        return 100.0

    # Split the texts into sets of words
    text_words = set(input_text.split())
    correct_words = set(correct_text.split())

    # Find the common words between the texts, and the incorrect words in the input text
    common_words = text_words & correct_words
    incorrect_words = text_words - common_words

    # Calculate the similarity ratio between the texts using SequenceMatcher
    seq = difflib.SequenceMatcher(None, input_text, correct_text)
    similarity = seq.ratio()

    # Calculate the final score, adjusting for the number of incorrect words in the input text
    score = max((similarity * 100.0) - (len(incorrect_words) * 100.0 / len(text_words)), 0.0)

    return score
