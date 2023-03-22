from datetime import datetime
import uuid
import pytz


# import spacy, re, nltk
# import collections

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

    def is_valid_username(text):
        
        # if text has no value
        if text ==  "":
            return False
        
        if len(text) < 3:
            return False
        
        return True

# Generate a random filename
class File:
    
    def name() -> str:
        # uses: uuid, pytz, datetime
        todays: datetime = datetime.now(pytz.timezone('Asia/Manila')).utcnow()
        utime: str = f'{uuid.uuid1()}{todays.hour}{todays.minute}{todays.second}'

        deduct: int = -2 if str(todays.year)[1] == '0' else -3
        udate: str = f"{str(todays.year)[deduct:]}{todays.month}{todays.day}"

        return f"{udate}{utime}"

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