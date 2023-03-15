from project.scripts.rate import rate_score

audio = "harvard.wav"
text = "The stale smell of old beer lingers. It takes heat to bring out the odor. A cold dip restores health and zest. A salt pickle tastes fine with ham. Taco's al pastor are my favorite. A zestful food is the hot cross bun."

rscore = rate_score(audio, text, use_temp_folder=False)
print("overall: ", rscore)