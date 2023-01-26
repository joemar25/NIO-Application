from flask import Flask, render_template, url_for
app = Flask(__name__)


@app.route("/")
def index():
    return 'return page'


@app.route("/record", methods=['GET'])
def record():
    return {"members": ["member1", "member2", "member3"]}


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
