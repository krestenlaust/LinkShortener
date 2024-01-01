import os
import psycopg2
import ssl
from flask import Flask, render_template, request, redirect, g
from rstr import xeger

import randomEmoji

app = Flask(__name__)

short_urls = {}


def get_db():
    if 'conn' not in g:
        g.conn = connect_db(os.environ['DATABASE_URL'])

    return g.conn


def connect_db(url):
    conn = psycopg2.connect(url, sslmode='require')
    with conn.cursor() as curs:
        curs.execute('''CREATE TABLE IF NOT EXISTS links(
        shortlink VARCHAR(2083) NOT NULL PRIMARY KEY,
        originallink VARCHAR(2083) NOT NULL
        );''')
        conn.commit()

    return conn


def set_url(short_link: str, original_link: str):
    conn = get_db()
    with conn.cursor() as curs:
        curs.execute("INSERT INTO links(shortlink, originallink) VALUES(%s, %s);", (short_link, original_link))
        conn.commit()


def get_url(short_link: str) -> str:
    conn = get_db()
    with conn.cursor() as curs:
        curs.execute("SELECT originallink FROM links WHERE shortlink = %s;", (short_link,))
        link = curs.fetchone()
        return link[0] if link is not None else "/"


def generate_url(emoji: bool):
    url = ""
    if emoji:
        for emoji in randomEmoji.emoji_generator(3):
            url += emoji
    else:
        url = xeger(r'[llΙI∣।ǀІ𐌠ⅼ౹ꞁ𐌉❘]{8}')

    return url


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route('/create', methods=['GET', 'POST'])
def create():
    original_url: str = request.form.get('originalurl')
    emoji_mode: bool = request.form.get('emoji') is not None
    generated_url = generate_url(emoji_mode)

    if not original_url.startswith('http://') and not original_url.startswith('https://'):
        original_url = "http://" + original_url

    set_url(generated_url, original_url)
    print(f"Generated new link: {generated_url} = {original_url}")
    return render_template("create.html", result=generated_url)


@app.route('/metoder/brainstorm', methods=['GET', 'POST'])
def brainstorm():
    return render_template("metoder/brainstorm.html")


@app.route('/<path:url>')
def other_urls(url):
    target_url = get_url(url)
    print(f"Asked {url} answered {target_url}.")

    return redirect(target_url, code=302)


if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations("ca.crt")
    context.load_cert_chain("public.key.pem", "private.key.pem")

    app.run(port=5000, ssl_context=context)
