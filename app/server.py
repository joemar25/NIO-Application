from flask import Flask, render_template, url_for
app = Flask(__name__)


@app.route("/")
def index():
    return 'return page'


'''
    this backend api, will be fetch by our front end for display
'''


@app.route("/feedback", methods=['GET'])
def feedback():
    # sample -> {"members": ["member1", "member2", "member3"]}

    rate = 80
    grammar = 81
    fluency = 85
    emotion = "Joyful"
    feedback = "this is a sample feedback"

    return {
        "rate": rate,
        "grammar": grammar,
        "fluency": fluency,
        "emotion": emotion,
        "feedback": feedback
    }


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
