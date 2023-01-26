from flask import Flask, render_template, request, url_for
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/index", methods=['POST'])
def sent():
    if request.method == "POST":
        user_name = request.form['username']
        user_script = request.form['text_script']
    return render_template("index.html", user_name=user_name, user_script=user_script)


'''
    this backend api, will be fetch by our front end for display
'''


@ app.route("/feedback", methods=['GET'])
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
    # debug=True is in development mode
