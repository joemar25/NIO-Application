import webbrowser
from project import app

if __name__ == "__main__":
    _port = 8080
    # webbrowser.open('https://nio-application.loca.lt')
    app.run(debug=True, threaded=True, host='0.0.0.0', port=_port)
