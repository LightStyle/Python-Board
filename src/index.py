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

from flask import Flask, render_template, Markup
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

if __name__ == '__main__':
    app.debug = True
    app.run()
