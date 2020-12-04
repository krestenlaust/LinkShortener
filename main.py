from flask import Flask, render_template, request, redirect, g
from rstr import xeger
import psycopg2
import os

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

    return conn


def set_url(short_link: str, original_link: str):
    conn = get_db()
    with conn.cursor() as curs:
        curs.execute('''INSERT INTO links(shortlink, originallink)
        VALUES(
            %s,
            %s
        );''', (short_link, original_link))


def get_url(short_link: str) -> str:
    conn = get_db()
    with conn.cursor() as curs:
        curs.execute('''SELECT `originallink` WHERE `shortlink`=%s''', short_link)
        link = curs.fetchone()
        return link if link is not None else "/"


def generate_url():
    return xeger(r'[li!ìíîïj|I†t1¦]{7,15}')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route('/create', methods=['GET', 'POST'])
def create():
    original_url = request.form.get('originalurl')
    generated_url = generate_url()

    if not original_url.startswith('http://') and not original_url.startswith('https://'):
        original_url = "http://" + original_url

    set_url(generated_url, original_url)
    print(f"Generated new link: {generated_url} = {original_url}")
    return render_template("create.html", result=generated_url)


@app.route('/<path:url>')
def other_urls(url):
    target_url = get_url(url)
    print(f"Asked {url} answered {target_url}.")

    return redirect(target_url, code=302)


if __name__ == '__main__':
    app.run(port=5000)
