from flask import Flask
from flask import render_template, request, redirect

from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, add_item 

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():

    items = get_items()
    return render_template('index.html', items=items)

@app.route('/new_item', methods=['POST'])
def new_item():
    new_item_title = request.form.get('new_item_title')
    items = add_item(new_item_title)
    return redirect('/')

if __name__ == '__main__':
    app.run()
