from flask import Flask
from flask import render_template, request, redirect
from operator import itemgetter
from todo_app.data.trello_api import archive_trello_card, get_trello_cards, get_trello_list_id, move_trello_card, create_trello_card
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():

    trello_list_ids = {}
    trello_list_ids['todo'] = get_trello_list_id('To Do')
    trello_list_ids['doing'] = get_trello_list_id('Doing')
    trello_list_ids['done'] = get_trello_list_id('Done')

    items = get_trello_cards()

    if request.values.get('sort') == '1':
        items = sorted(items, key=itemgetter('idList','name'))
    elif request.values.get('sort') == '2':
        items = sorted(items, key=itemgetter('idList','name'), reverse=True)

    return render_template('index.html', items=items,trello_list_ids=trello_list_ids)


@app.route('/new_item', methods=['POST'])
def new_item():
    new_item_title = request.form.get('new_item_title')
    create_trello_card(new_item_title)
    return redirect(request.headers.get('Referer'))


@app.route('/archive_item', methods=['POST'])
def remove_existing_item():
    archive_id = request.form.get('archive_item_id')
    archive_trello_card(archive_id)
    return redirect(request.headers.get('Referer'))


@app.route('/toggle_status', methods=['POST'])
def toggle_status():
    trello_card_id = request.form.get('toggle_item_id')
    new_trello_list_id = request.form.get('new_trello_list_id')

    move_trello_card(trello_card_id,new_trello_list_id)

    return redirect(request.headers.get('Referer'))

if __name__ == '__main__':
    app.run()
