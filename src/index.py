# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Python Board FF-Style
#
# Copyright (C) 2010 Niccolò "Kid" Campolungo <damnednickix@hotmail.it>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#

import re

from flask import *
from pymongo import *

app = Flask(__name__)
run_port = 80

db = Connection().ff

@app.route("/")
def index():
    return 'Index page'

@app.route("/topic/<id>")
def topic(id):
    topic_dict = db.topics.find_one({'id': id})
    topic_title = "Errore"
    try:
        topic_title = topic_dict['title']
        topic_author_id = topic_dict['author']
        topic_author_dict = db.users.find_one({'id': topic_author_id})
        if topic_author_dict:
            topic_author_nick = topic_author_dict['nick']
        topic_id = topic_dict['id']
        topic_desc = topic_dict['desc']
        topic_content = topic_dict['content']
    except:
        pass
    return render_template('topic.html', **locals())

@app.route("/section/<id>")
def section(id):
    query_string = url[url.find('?'):]
    return '{url}<br />{base_url}<br />{q_s}'.format(url=url,
                                                     base_url=base_url,
                                                     q_s=query_string)

@app.route("/user/<id>")
def user(id):
    user_dict = db.users.find_one({'id': id})
    user_title = "Errore"
    try:
        user_nick = user_dict['nick']
        user_avatar_url = user_dict['avatar']
        user_avatar = Markup('<img src="{avatar}" />'.format(avatar=user_avatar_url))
        user_title = "Profilo di {nick}".format(nick=user_nick)
        user_id = id
        user_email = user_dict['email']
        user_admin = user_dict['admin']
        user_admin_str = user_admin and "L'utente {nick} e' un admin del sito".format(nick=user_nick) or ''
    except:
        pass
    return render_template('user.html', **locals())

@app.route("/test/recv/", methods = ['POST'])
def recv():
    try:
        args = request.form
        login = args['login']
        password = args['password']
        logged = 'False'
        if check_email(login):
            tosearch = 'email'
        elif login.isdigit():
            tosearch = 'id'
        else:
            tosearch = 'nick'
        login_dict = db.users.find_one({tosearch: login})
        if login_dict:
            db_pw = login_dict['password']
            if password == db_pw:
                logged = 'True'
        return 'Login: {0}<br />\nPassword: {1}<br />\nLogged: {2}'.format(login,
                                                                           password,
                                                                           logged)
    except:
        pass

@app.route("/test/send/")
def send():
    return render_template('send.html')

def check_email(string):
    return bool(re.match('([A-Za-z0-9]*)@([A-Za-z0-9]*).([a-z]*)', string))

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=run_port)
