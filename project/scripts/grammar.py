import nltk, difflib
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
class Grammar:

  def __init__(self):
    
    if not nltk.download('punkt', quiet=True):
      nltk.download('punkt')
    
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

  def __correct(self, input_sentence, max_candidates=1):
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


  def correct(self, input_sentence):
    input = self.__correct(input_sentence)

    # Capitalize the first letter of the first word
    text = input[0].upper() + input[1:]

    # Check if the last character is a punctuation mark
    if not text.endswith(('.', '?', '!')):
        # If not, add a period at the end
        text += '.'

    return text

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

# b = Grammar()
# a = b.checkGrammar("incorrect grammar here")
# print(a)
