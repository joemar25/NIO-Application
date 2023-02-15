import spacy, re, nltk
import collections


class Validation:
    
    __ALLOWED_EXTENSIONS = {'txt'}    

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in self.__ALLOWED_EXTENSIONS
    
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
        
        # https://www.dataquest.io/blog/tutorial-text-classification-in-python-using-spacy/
        
        return True


class Logs():
    """
    eveytime we create a record it will put it in a file.txt
    everyime we end the program we erase the contents of that
    """

    def create(name: str, scores: dict, feedback: str) -> str:
        pass

    def destroy() -> None:
        pass

# sentence = """As far as the laws of mathematics refer to reality they are not certain as far as they are certain they do not refer to reality"""

# text = [
#     "",
#     "is a great",
#     "a is a great warrior",
#     "a is a great warrior.",
#     "A is a great warrior.",
#     "Luffy is a great warrior.",
#     "a a a a aa a.",
#     "a a a a aa a",
# ]

# res = Validation.is_valid_sentence(text[2])
# print(res)