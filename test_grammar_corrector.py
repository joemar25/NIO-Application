from project.scripts.grammar import Grammar as grammar
from project.scripts.grammar import grammar_score

sentences = [
    "I have visited Niagara Falls last weekend.",
    "The woman which works here is from Japan.",
    "She's married with a dentist.",
    "She was boring in the class.",
    "I must to call him immediately.",
    "Every students like the teacher.",
    "Although it was raining, but we had the picnic.",
    "I enjoyed from the movie.",
    "I look forward to meet you.",
    "I like very much ice cream.",
]

for text in sentences:
    
    c_text = grammar().correct(text)
    g_score = grammar_score(text, c_text)
    
    print("incorrect:", text)
    print("correct  :", c_text)
    print("score    :", g_score, "\n")
