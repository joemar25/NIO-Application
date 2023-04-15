class Feedback:
    """
    A class that generates feedback based on a speaker's performance in a conversation or interview.

    Attributes:
        rate (dict): A dictionary containing the score and label for the speaker's speaking rate.
        grammar (float): The speaker's score for grammar, measured as a percentage.
        fluency (float): The speaker's score for fluency, measured as a percentage.
    """

    def __init__(self, rate, grammar, fluency):
        """
        Initializes a new instance of the Feedback class with the given rate, grammar, and fluency scores.

        Args:
            rate (dict): A dictionary containing the score and label for the speaker's speaking rate.
            grammar (float): The speaker's score for grammar, measured as a percentage.
            fluency (float): The speaker's score for fluency, measured as a percentage.
        """
        self.rate = rate
        self.grammar = grammar
        self.fluency = fluency
    
    def rate_comment(self):
        """
        Generates feedback on the speaker's speaking rate.

        Returns:
            A string containing feedback on the speaker's speaking rate.
        """
        if self.rate["label"] == "slow":
            return "Your performance speed could be improved. You may want to try speaking more confidently and clearly to help speed up your responses."
        elif self.rate["label"] == "fast":
            return "Your performance speed is impressive, but you could benefit from taking more time to think through your responses. Try to take a breath and gather your thoughts before speaking."
        elif self.rate["label"] == "ideal":
            return "Your performance speed is ideal. Well done! You have a good balance of speaking at a comfortable pace while still answering questions effectively."
        else:
            return "The performance speed label provided is invalid. Please provide a value of 'slow', 'fast', or 'ideal'."

    def grammar_comment(self):
        """
        Generates feedback on the speaker's grammar.

        Returns:
            A string containing feedback on the speaker's grammar.
        """
        if self.grammar >= 90:
            return "It is excellent! You consistently use proper grammar and have a great understanding of grammar rules."
        elif 80 <= self.grammar < 90:
            return "It is good, but there is room for improvement. You have a good grasp of grammar rules, but there are some errors in your usage."
        else:
            return "It grammar needs significant improvement. Please review grammar rules and practice more. There are many errors in your usage and it is affecting your overall communication."    

    def fluency_comment(self):
        """
        Generates feedback on the speaker's fluency.

        Returns:
            A string containing feedback on the speaker's fluency.
        """
        if self.fluency >= 90:
            return "Your speech is very fluent and natural."
        elif 80 <= self.fluency < 90:
            return "Your speech is mostly fluent, but there are some areas for improvement."
        else:
            return "Your speech needs significant improvement in terms of fluency. Please practice speaking more and work on reducing the number of fillers."
    
    def feedback(self):
        """
        Generates overall feedback on the speaker's performance.

        Returns:
            A string containing feedback on the speaker's performance, including rate, grammar, and fluency.
        """
        rate_comment = str(self.rate_comment()).lower()
        grammar_comment = str(self.grammar_comment()).lower()
        fluency_comment = str(self.fluency_comment()).lower()

        feedback_message = "In terms of rate, {}\n".format(rate_comment)
        feedback
