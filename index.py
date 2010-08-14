from flask import Flask, render_template, send_file
from logging import Formatter

app = Flask(__name__)

@app.route("/")
def index():
    return 'Index page'

@app.route("/topic/<id>")
def topic(id):
    return 'Topic con id {id}'.format(id=id)

@app.route("/section/<id>")
def section(id):
    return 'Sezione con id {id}'.format(id=id)

@app.route("/user/<id>")
def user(id):
    return 'Utente con id {id}'.format(id=id)

if __name__ == '__main__':
    app.debug = True
    app.run()
