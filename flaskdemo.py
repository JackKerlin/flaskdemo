"""
CP1404 Practical Jack Kerlin
Wiki api
Estimate: 1 hour
Actual: 40 minutes to do the listed stuff, and another 40 to add the random and language feature
"""

from flask import Flask, render_template, request, redirect, url_for, session
import wikipedia

app = Flask(__name__)
# Set the secret key. Keep this really secret:
app.secret_key = 'IT@JCUA0Zr98j/3yXa R~XHH!jmN]LWX/,?RT'


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/random')
def random():
    current_language = set_language()
    wikipedia.set_lang(current_language)
    page = wikipedia.page(wikipedia.random())
    return render_template("results.html", page=page)


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        session['search_term'] = request.form['search']
        return redirect(url_for('results'))
    return render_template("search.html")


@app.route('/results')
def results():
    search_term = session['search_term']
    current_language = set_language()
    page = get_page(search_term, current_language)
    return render_template("results.html", page=page)


@app.route('/language', methods=['POST', 'GET'])
def language():
    if request.method == 'POST':
        session['language'] = request.form['submit_button']
        return render_template('home.html')
    elif request.method == 'GET':
        return render_template('language.html')
    return render_template('language.html')


def set_language():
    current_language = session['language']
    if not current_language:
        current_language = "en"
    return current_language

def get_page(search_term, current_language):
    wikipedia.set_lang(current_language)
    try:
        page = wikipedia.page(search_term)
    except wikipedia.exceptions.PageError:
        # no such page, return a random one
        page = wikipedia.page(wikipedia.random())
    except wikipedia.exceptions.DisambiguationError:
        # this is a disambiguation page, get the first real page (close enough)
        page_titles = wikipedia.search(search_term)
        # sometimes the next page has the same name (different caps), so don't try the same again
        if page_titles[1].lower() == page_titles[0].lower():
            title = page_titles[2]
        else:
            title = page_titles[1]
        page = get_page(wikipedia.page(title), current_language)
    return page


if __name__ == '__main__':
    app.run()
