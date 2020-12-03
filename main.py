from flask import Flask, render_template, request, redirect
import rstr

app = Flask(__name__)


short_urls = {}


def generate_url():
    return rstr.xeger(r'[a-z]{100}')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/create', methods=['GET', 'POST'])
def create():
    original_url = request.form.get('originalurl')
    new_url = generate_url()
    short_urls[new_url] = original_url
    return render_template("create.html", result=new_url)

@app.route('/<path:url>')
def other_urls(url):
    try:
        return redirect(short_urls[url], code=302)
    except:
        return redirect('/', code=302)


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
    
