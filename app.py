from flask import Flask
from sayhello import views
app = Flask(__name__)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
