#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
from flask import Flask, g, request, render_template, redirect, jsonify, abort
from flask.ext.redis import FlaskRedis
from werkzeug.routing import BaseConverter

app = Flask(__name__)
app.config.update(dict(
    WORDS_PATH = os.path.join(app.root_path, 'words.txt'),
    REDIS_URL = 'redis://:password@localhost:6379/0',
))

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter


def get_redis():
    if not hasattr(g, 'redis'):
        if app.testing:
            rs = FlaskRedis.from_custom_provider(app.config['REDIS_PROVIDER'])
        else:
            rs = FlaskRedis()

        rs.init_app(app)
        g.redis = rs

    return g.redis


def padkey(padname, prefix='pad'):
    return '%s:%s' % (prefix, padname)


@app.route('/<regex("\w+"):padname>', methods=['GET'])
def get(padname):
    content = get_redis().get(padkey(padname))
    if not content:
        content = ''

    return render_template('main.html', padname=padname, content=content.decode('utf-8'))


@app.route('/<regex("\w+"):padname>', methods=['POST'])
def set(padname):
    content = request.form['t']
    if not content:
        abort(401)

    get_redis().set(padkey(padname), content)
    return jsonify(message='ok', padname=padname)


@app.route('/')
def main():
    words = open(app.config['WORDS_PATH'], 'r').read().splitlines()
    word = words.pop(random.randrange(len(words)))

    while get_redis().exists(padkey(word)):
        word += str(random.randrange(10))

    return redirect('/%s' % word)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
