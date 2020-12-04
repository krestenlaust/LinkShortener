from flask import Flask, render_template, request, redirect
from rstr import xeger
from urllib.parse import quote, unquote

app = Flask(__name__)


short_urls = {}


def generate_url():
    return xeger(r'[li!ìíîïj|I†t1¦]{7,15}')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route('/create', methods=['GET', 'POST'])
def create():
    original_url = request.form.get('originalurl')
    generated_url = generate_url()
    i = 0
    while generated_url in short_urls and i < 100:
        generated_url = generate_url()
        i += 1

    if not original_url.startswith('http://') and not original_url.startswith('https://'):
        original_url = "http://" + original_url

    print(f"Generated new link: {generated_url} = {original_url}")
    short_urls[generated_url] = original_url
    return render_template("create.html", result=generated_url)


@app.route('/<path:url>')
def other_urls(url):
    if url in short_urls:
        print("Found reference")
        return redirect(short_urls[url], code=302)

    print(short_urls)
    print("Unknown: " + url)
    return redirect('/', code=302)


if __name__ == '__main__':
    app.run(port=5000)
