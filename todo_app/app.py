from flask import Flask
from flask import render_template, request, redirect
from operator import itemgetter

from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, add_item, save_item, get_item, remove_item

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():

    items = get_items()
    if request.values.get('sort') == '1':
        items = sorted(items, key=itemgetter('status'))
    elif request.values.get('sort') == '2':
        items = sorted(items, key=itemgetter('status'), reverse=True)
    else:
        items = sorted(items, key=itemgetter('id'))

    return render_template('index.html', items=items)

@app.route('/new_item', methods=['POST'])
def new_item():
    new_item_title = request.form.get('new_item_title')
    items = add_item(new_item_title)
    return redirect('/')

@app.route('/remove_item', methods=['POST'])
def remove_existing_item():
    remove_id = request.form.get('remove_id')
    items = remove_item(remove_id)
    return redirect('/')

@app.route('/toggle_status', methods=['POST'])
def toggle_status():
    toggle_item = get_item(request.form.get('toggle_item_id'))

    if toggle_item['status'] == "Not Started":
        toggle_item['status'] = "Completed"
    else:
        toggle_item['status'] = "Not Started"

    item = save_item(toggle_item)
    return redirect('/')

if __name__ == '__main__':
    app.run()
