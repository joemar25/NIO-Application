from gingerit_class import Grammar as grammar

text1 = """At the start of  school Dora was afrad of  her new Teacher. Mrs. Davis seamed nice, but she had so manny rules for the class to folow. Scare someone to pieces. As the school year cotinued, Dora begun to understan how the Teacher come up with the rules The rules were their so students would be respecful of  theyselves and each other. By the end of  the year, Dora though Mrs. Davis was the best Teacher she evere had!"""
text2= """A greenhouse is a glass building used to grow plants. A greenhouse has transparent glass that allows the sunlight to pass through, but does not allow the heat inside to escape. The same affect occurs on the earth. The suns radiation passes through the atmosphere to heat the earth's surface. When heated, the earth's surface produces infrared radiation, which has a longer wavelength than that of sunlight. This infrared radiation rises into the atmosphere where gases, such as carbon dioxide, prevents the infrared radiation from escaping into space. The concentrations of these gases which are called greenhouse gases, control how much infrared radiation escapes. The retained radiation heats the earth's atmosphere, thus keeping the planet warm."""
text3= """During the last century, the concentrations of greenhouse gases have increased substantially [Holman, 1985]. Scientists believe that further increases could cause excess warming of the earth's climate. Moreover, many scientists believe this warming could produce side effects. For example, the changing of the earth's wind patterns. These wind patterns control the amount of rain received in a particular area. If the greenhouse gases warm the earth's climate too much, areas that now receive plenty of rainfall could become deserts, moreover, some scientists speculate that additional increases in warming could cause another effect, a rise in the ocean levels ["Greenhouse," 1990]. How would this rise occur? An increase in global temperature would melt the polar ice caps, thus emptying more water into the oceans. They also predict that this ocean rise, which may be as high as 1 meter could flood port cities and coastal lands."""

sample = grammar(text1)
print(sample.checkGrammar())




