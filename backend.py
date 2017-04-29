from flask import *
from api_url import api

app = Flask(__name__)
app.register_blueprint(api.blueprint)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/topic')
def topic():
    return render_template("topic.html")


@app.route('/edit')
def edit():
    return render_template("edit.html")


@app.route('/add')
def add():
    return render_template("add.html")


if __name__ == '__main__':
    """
    browser-sync start -p "127.0.0.1:5000" -f "../cheatsheet_generate"
    """
    app.run(debug=True)
