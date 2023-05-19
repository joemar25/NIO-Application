class Feedback:
    """
    A class that generates feedback based on a speaker's performance in a conversation or interview.

    Attributes:
        rate (dict): A dictionary containing the score and label for the speaker's speaking rate.
        grammar (float): The speaker's score for grammar, measured as a percentage.
        fluency (float): The speaker's score for fluency, measured as a percentage.
    """

    def __init__(self, rate=0, grammar=0, fluency=0):
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
        if self.rate < 50:
            return "your speaking rate needs improvement. You may want to try speaking more confidently and clearly to help speed up your responses."

        if self.rate >= 50 and self.rate < 80:
            return "your speaking rate is good, but there is room for improvement. You could benefit from taking more time to think through your responses. Try to take a breath and gather your thoughts before speaking."

        if self.rate >= 80:
            return "your speaking rate is ideal. Well done! You have a good balance of speaking at a comfortable pace while still answering questions effectively."
        
    def grammar_comment(self):
        """
        Generates feedback on the speaker's grammar.

        Returns:
            A string containing feedback on the speaker's grammar.
        """
        if self.grammar >= 90:
            return "it is excellent! You consistently use proper grammar and have a great understanding of grammar rules."
        elif 80 <= self.grammar < 90:
            return "it is good, but there is room for improvement. You have a good grasp of grammar rules, but there are some errors in your usage."
        else:
            return "it grammar needs significant improvement, please review grammar rules and practice more, there are many errors in your usage and it is affecting your overall communication."

    def fluency_comment(self):
        """
        Generates feedback on the speaker's fluency.

        Returns:
            A string containing feedback on the speaker's fluency.
        """
        if self.fluency >= 90:
            return "your speech is very fluent and natural."
        elif 80 <= self.fluency < 90:
            return "your speech is mostly fluent, but there are some areas for improvement."
        else:
            return "your speech needs significant improvement in terms of fluency. Please practice speaking more and work on reducing the number of fillers."
    
    def feedback(self):
        """
        Generates overall feedback on the speaker's performance.

        Returns:
            A string containing feedback on the speaker's performance, including rate, grammar, and fluency.
        """
        rate_comment = str(self.rate_comment())
        grammar_comment = str(self.grammar_comment())
        fluency_comment = str(self.fluency_comment())

        feedback_message = "In terms of rate, {} ".format(rate_comment)
        feedback_message += "In terms of grammar, {} ".format(grammar_comment)
        feedback_message += "Regarding fluency, {} ".format(fluency_comment)

        return feedback_message
    
    @property
    def rate(self):
        return self._rate
    
    @rate.setter
    def rate(self, value):
        self._rate = value
    
    @property
    def grammar(self):
        return self._grammar
    
    @grammar.setter
    def grammar(self, value):
        self._grammar = value
    
    @property
    def fluency(self):
        return self._fluency
    
    @fluency.setter
    def fluency(self, value):
        self._fluency = value