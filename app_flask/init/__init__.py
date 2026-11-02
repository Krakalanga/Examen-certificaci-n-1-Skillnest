from flask import Flask


def app():
    app = Flask(__name__, template_folder = '../views')
    app.secret_key = '12345'
    return app

