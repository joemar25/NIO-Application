from project import app

if __name__ == "__main__":
    _port = 8080
    app.run(debug=False, threaded=True, host='0.0.0.0', port=_port)
