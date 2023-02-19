from project import app

if __name__ == "__main__":

    """
        port=8080 is important for us; when connecting to the client's frontent we will
        configure package.json and set the to "proxy": "http://127.0.0.1:8080" since we use
        8080 else just put the "proxy": "http://127.0.0.1:5000" since it is the default proxy
    """
    
    app.run(debug=True, threaded=True, host='localhost', port=8080)
