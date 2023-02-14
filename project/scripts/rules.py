from wtforms.validators import Length, ValidationError

class Validation:
    
    ALLOWED_EXTENSIONS = {'txt'}    
    
    def validate_text(self, input) -> bool:
        """
        splitting result in world by world counting
        putting it to n  and  analyze
        n must be greater than 3
        and must be less than 5000
        """
        
        text = input.data
        split = text.split()
        n = len(split)
        if not (n > 3 and n < 5000):
            raise ValidationError('not a valid sentence for speech. try again')
        return

class Logs():
    """
    eveytime we create a record it will put it in a file.txt
    everyime we end the program we erase the contents of that
    """

    def create(name: str, scores: dict, feedback: str) -> str:
        pass

    def destroy() -> None:
        pass


"""
    testing below
"""
# def main() -> None:
#     validate = Validation
#     err = Errors
#     name = "joemar"
#     text = "this is a sentence."

#     res = validate.name(name)
#     print("is valid name length = ", res)
#     print(err.name_input(res))

#     print()
#     res = validate.text(text)
#     print("is valid text length = ", res)
#     print(err.text_input(res))

# if __name__ == "__main__":
#     main()
