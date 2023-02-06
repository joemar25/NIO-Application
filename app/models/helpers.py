class Validation():
    """
        Validation class for validating functions
    """

    def name(input: str) -> bool:
        """
            name must be greater than 3
            and not longer than 20 characters

            need improvement incase, puro space nilagay
        """
        input = input.replace(" ", "")
        n = len(input)
        return n > 2 and n < 21

    def text(input: str) -> bool:
        """
            splitting result in world by world counting
            putting it to n  and  analyze
            n must be greater than 3
            and must be less than 5000
        """
        split = input.split()
        n = len(split)
        return n > 3 and n < 5000


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
