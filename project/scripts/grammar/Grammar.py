import nltk
import difflib
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

if not nltk.download('punkt', quiet=True):
    nltk.download('punkt')

correction_model_tag = "prithivida/grammar_error_correcter_v1"
correction_tokenizer = AutoTokenizer.from_pretrained(
    correction_model_tag, use_auth_token=False)
correction_model = AutoModelForSeq2SeqLM.from_pretrained(
    correction_model_tag, use_auth_token=False)


class Grammar:
    def __init__(self):
        self.sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

    def corrector(self, input_sentence, max_candidates=1):
        input_ids = correction_tokenizer.encode(
            "gec: " + input_sentence, return_tensors='pt')

        preds = correction_model.generate(
            input_ids,
            do_sample=True,
            max_length=128,
            num_beams=7,
            early_stopping=True,
            num_return_sequences=max_candidates
        )

        corrected = set(correction_tokenizer.decode(
            pred, skip_special_tokens=True).strip() for pred in preds)
        return list(corrected)[0] if corrected else None

    def correct(self, sentences):
        if not sentences:
            return ''
        cache = {}
        result = []
        for sentence in sentences.split('.'):
            sentence = sentence.strip()
            if sentence:
                if sentence in cache:
                    corrected = cache[sentence]
                else:
                    corrected = self.corrector(sentence)
                    cache[sentence] = corrected
                remove_extra = re.sub(
                    r'[^\w\s]+', lambda m: m.group(0)[0], corrected).rstrip('.')
                if not remove_extra.endswith((".", "!", "?")):
                    remove_extra += "."

                result.append(remove_extra)
        corrected_sentence = ' '.join(result)
        return corrected_sentence


def grammar_score(input_text, correct_text):
    if input_text == correct_text:
        return 100.0
    text_words = set(input_text.split())
    correct_words = set(correct_text.split())
    common_words = text_words & correct_words
    incorrect_words = text_words - common_words
    seq = difflib.SequenceMatcher(None, input_text, correct_text)
    similarity = seq.ratio()
    score = max((similarity * 100.0) -
                (len(incorrect_words) * 100.0 / len(text_words)), 0.0)
    return score
