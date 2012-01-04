#!/usr/bin/env python
# coding=utf8

from base64 import urlsafe_b64encode, urlsafe_b64decode
from hashlib import sha256
from itertools import count
from random import SystemRandom
from struct import pack, unpack

from flask import Flask, render_template, request, current_app, abort

MAX_SECRET_LENGTH = 512
KEY_BITS = 64  # fits into Q
MAX_SECRETS_STORED = (5*1024*1024)/MAX_SECRET_LENGTH  # 5 M max

r = SystemRandom()

# global storage
secrets = {}
secret_id_list = []

app = Flask(__name__)
app.config.from_object(__name__)

def enc_int(i):
    return urlsafe_b64encode(pack('!Q', i))


def dec_int(s):
    return unpack('!Q', urlsafe_b64decode(s))[0]


def cycling_counter(limit):
    while True:
        for i in xrange(limit):
            yield i


# reasonably avoid collisions
counter = cycling_counter(max(MAX_SECRETS_STORED, 2**16))


@app.route('/s/<int:id>/', methods=('GET', 'POST'))
def show_secret(id):
    try:
        key, secret  = secrets[id]
    except KeyError:
        abort(404)

    if 'POST' == request.method:
        # check if the key is correct
        try:
            user_key = dec_int(str(request.form['key']))
        except (TypeError, UnicodeDecodeError):
            return render_template('show.html', error=u"Bad key")

        if key != user_key:
            return render_template('show.html', error=u"Wrong key")

        # all good, reveal
        return render_template('reveal.html', id=id, key=key, secret=secret)
    else:
        return render_template('show.html')


@app.route('/', methods=('GET', 'POST'))
def index():
    if 'POST' == request.method:
        secret = request.form['secret']

        if len(secret) > current_app.config['MAX_SECRET_LENGTH']:
            return render_template('index.html', error='secret too large')
        else:
            # prune secrets
            if len(secret_id_list) == MAX_SECRETS_STORED:
                rem = secret_id_list.pop(0)
                del secrets[rem]

            # generate secret id and key
            id = counter.next()
            key = r.getrandbits(KEY_BITS)

            secrets[id] = (key, secret)
            secret_id_list.append(id)

            return render_template('done.html',
                                   id=id,
                                   key64=enc_int(key))

    return render_template('index.html')


if '__main__' == __name__:
    app.run(debug=True)
