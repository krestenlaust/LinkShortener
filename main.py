from flask import Flask, render_template, request, redirect
from rstr import xeger

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

    print(f"Generated new link: {generated_url} = {original_url}")
    short_urls[generated_url] = original_url
    return render_template("create.html", result=generated_url)

@app.route('/<path:url>')
def other_urls(url):
    try:
        return redirect(short_urls[url], code=302)
    except:
        return redirect('/', code=302)


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
    
