import spacy, re, nltk
import collections

def getPercent(first, second, integer = False):
   percent = first / second * 100
   
   if integer:
       return int(percent)
   return percent

# print(getPercent(9, 9, True))

def is_valid_sentence(text):
    
    # if text has no value
    if text ==  "":
        return False
    
    # edit the constant 3 for more classification of a specific sentence that matter to the speech 
    if len(text.split()) < 3:
        return False
    
    # a a a aa a. or 
    # we can ignore if we want the .
    words = text.split()
    word_counts = collections.Counter(words)
    twc = sum(word_counts.values()) # total world count
    count_list = []
    for word, count in sorted(word_counts.items()):
        # print('"%s" is repeated %d time%s.' % (word, count, "s" if count > 1 else ""))
        count_list.append(count)
        
    h = max(count_list) # highest
    # pag 50% lagpas meaning repeatative talaga ung text meaning error ang ibalik or false
    res = getPercent(h, twc, True)
    if res > 50:
        return False
    
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(text)
        # Define regex pattern for sentence
        pattern = r'^[a-zA-Z][\w\s,:;\'"`-]*[.?!]$'

        # Tokenize the text into words and remove any non-word characters
        tokens = nltk.word_tokenize(text)
        words = [word for word in tokens if word.isalpha()]

        # Check if sentence matches pattern and contains only valid words
        match = re.search(pattern, text)
        if match is None or len(words) == 0:
            return False
    
    return True



class Validation:
    
    ALLOWED_EXTENSIONS = {'txt'}    

    def is_valid_sentence(text):
        return False

class Logs():
    """
    eveytime we create a record it will put it in a file.txt
    everyime we end the program we erase the contents of that
    """

    def create(name: str, scores: dict, feedback: str) -> str:
        pass

    def destroy() -> None:
        pass

sentence = """As far as the laws of mathematics refer to reality they are not certain as far as they are certain they do not refer to reality"""

text = [
    "",
    "is a great",
    "a is a great warrior",
    "a is a great warrior.",
    "A is a great warrior.",
    "Joemar is a great warrior.",
    "a a a a aa a.",
    "a a a a aa a",
]

# test = Validation.is_valid_sentence(text)
res = is_valid_sentence(text[0])
print(res)
res = is_valid_sentence(text[1])
print(res)
res = is_valid_sentence(text[2])
print(res)
res = is_valid_sentence(text[3])
print(res)
res = is_valid_sentence(text[4])
print(res)
res = is_valid_sentence(text[5])
print(res)
res = is_valid_sentence(text[6])
print(res)
res = is_valid_sentence(text[7])
print(res)

res = is_valid_sentence(sentence)
print(res)
