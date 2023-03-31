# from pyngrok import ngrok
from project import app

_port = 8080
# ngrok.set_auth_token(os.getenv('NGROK_KEY'))
# public_url = ngrok.connect(_port).public_url

if __name__ == "__main__":
    # print("Access Link:", public_url)
    app.run(debug=True, threaded=True, host='0.0.0.0', port=_port)
