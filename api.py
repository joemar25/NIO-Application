from project import app
# import webbrowser

_port = 8000
url = 'https://nio-application.loca.lt'

if __name__ == "__main__":
    # webbrowser.open(url)
    app.run(debug=False, threaded=True, host='0.0.0.0', port=_port)
