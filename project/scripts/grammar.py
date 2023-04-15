"""
Grammar class to correct grammatical errors in the input sentence and
calculate the grammar score of input and correct sentences.

Attributes:

correction_tokenizer: tokenizer to encode input sentence before passing to
correction_model for grammatical correction.
correction_model: model to correct grammatical errors.
device: device on which the correction_model is loaded.
model_loaded: boolean variable to check if the correction_model is loaded.
Methods:

init(self): Constructor method to initialize Grammar class attributes.
correct(self, input_sentence, max_candidates=1): Method to correct grammatical
errors in input_sentence using correction_model.
grammar_score(input_text, correct_text): Method to calculate grammar score
of input_text and correct_text using similarity ratio of text_words and
correct_words, and count of incorrect_words.
Usage:
grammar = Grammar()
corrected_sentence = grammar.correct("He go to school")
grammar_score = grammar.grammar_score("He go to school", "He goes to school")
"""

import nltk, difflib
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

if not nltk.download('punkt', quiet=True):
  nltk.download('punkt')

class Grammar:

  def __init__(self):
    
    correction_model_tag = "prithivida/grammar_error_correcter_v1"
    device = "cpu"

    self.sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    self.device = device
    self.model_loaded = False

    try:
      self.correction_tokenizer = AutoTokenizer.from_pretrained(correction_model_tag, use_auth_token=False)
      self.correction_model     = AutoModelForSeq2SeqLM.from_pretrained(correction_model_tag, use_auth_token=False)
      self.correction_model     = self.correction_model.to(device)
      self.model_loaded = True
    except Exception as e:
      ...

  def correct(self, input_sentence, max_candidates=1):
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