from flask import Flask, render_template
from pymongo import *

app = Flask(__name__)

db = Connection().ff

@app.route("/")
def index():
    return 'Index page'

@app.route("/topic/<id>")
def topic(id):
    topic_dict = db.topics.find_one({'id': id})
    topic_title = "Errore"
    if topic_dict:
        topic_title = topic_dict['title']
        topic_author_id = topic_dict['author']
        topic_author_dict = db.users.find_one({'id': topic_author_id})
        if topic_author_dict:
            topic_author_nick = topic_author_dict['nick']
        topic_id = topic_dict['id']
        topic_desc = topic_dict['desc']
        topic_content = topic_dict['content']
        return render_template('topic.html', **locals())
    else:
        return render_template('topic.html', **locals())

@app.route("/section/<id>")
def section(id):
    return 'Sezione con id {id}'.format(id=id)

@app.route("/user/<id>")
def user(id):
    user_dict = db.users.find_one({'id': id})
    user_title = "Errore"
    if user_dict:
        user_nick = user_dict['nick']
        user_title = "Profilo di {nick}".format(nick=user_nick)
        user_id = id
        user_email = user_dict['email']
        user_admin = user_dict['admin']
        user_admin_str = user_admin and "L'utente {nick} e' un admin del sito".format(nick=user_nick) or ''
        return render_template('user.html', **locals())
    else:
        return render_template('user.html', **locals())

if __name__ == '__main__':
    app.debug = True
    app.run()
