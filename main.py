from src.api import restAPI
from flask import Flask

app = Flask(__name__)
app.register_blueprint(restAPI)


if __name__ == '__main__':
    app.run(debug=True)