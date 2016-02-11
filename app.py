#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
from flask import Flask, request, render_template, redirect, jsonify, abort
from flask.ext.redis import FlaskRedis

app = Flask(__name__)
app.APP_PATH = os.path.dirname(os.path.realpath(__file__))
app.WORDS_PATH = os.path.join(app.APP_PATH, 'words.txt')
app.REDIS_URL = "redis://localhost:6379/0"  # redis://:password@localhost:6379/0

redis_store = FlaskRedis(app)


def padkey(padname, prefix='pad'):
    return '%s:%s' % (prefix, padname)


@app.route('/<padname>', methods=['GET'])
def get(padname):
    content = redis_store.get(padkey(padname))
    if not content:
        content = ''

    return render_template('main.html', padname=padname, content=content)


@app.route('/<padname>', methods=['POST'])
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
    app.run(debug=True)
