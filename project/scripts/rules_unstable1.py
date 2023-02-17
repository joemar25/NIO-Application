import re
import nltk

class Validation:
    
    ALLOWED_EXTENSIONS = {'txt'}    
    
    def is_valid_sentence(text):
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
#     return False
# the last value of the text must not be 1 char

class Logs():
    """
    eveytime we create a record it will put it in a file.txt
    everyime we end the program we erase the contents of that
    """

    def create(name: str, scores: dict, feedback: str) -> str:
        pass

    def destroy() -> None:
        pass

text = "My oemar."
test = Validation.is_valid_sentence(text)

print(test)