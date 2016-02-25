#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
from flask import Flask, request, render_template, redirect, jsonify, abort
from flask.ext.redis import FlaskRedis
from werkzeug.routing import BaseConverter

app = Flask(__name__)
app.APP_PATH = os.path.dirname(os.path.realpath(__file__))
app.WORDS_PATH = os.path.join(app.APP_PATH, 'words.txt')
app.REDIS_URL = "redis://localhost:6379/0"  # redis://:password@localhost:6379/0

redis_store = FlaskRedis(app)


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter


def padkey(padname, prefix='pad'):
    return '%s:%s' % (prefix, padname)


@app.route('/<regex("\w+"):padname>', methods=['GET'])
def get(padname):
    content = redis_store.get(padkey(padname))
    if not content:
        content = ''

    return render_template('main.html', padname=padname, content=content)


@app.route('/<regex("\w+"):padname>', methods=['POST'])
def set(padname):
    content = request.form['t']
    if not content:
        abort(401)

    redis_store.set(padkey(padname), content)
    return jsonify(message='ok', padname=padname)


@app.route('/')
def main():
    words = open(app.WORDS_PATH, 'r').read().splitlines()
    word = words.pop(random.randrange(len(words)))

    while redis_store.exists(padkey(word)):
        word += str(random.randrange(10))

    return redirect('/%s' % word)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
