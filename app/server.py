from flask import Flask, render_template, url_for
app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('index.html')


@app.route("/members")
def members():
    return {"members": ["member1", "member2", "member3"]}


if __name__ == "__main__":
    # debug mode is here since we are in dev mode
    app.run(debug=True)
