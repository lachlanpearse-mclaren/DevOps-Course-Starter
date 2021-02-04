from flask import Flask
from flask import render_template, request, redirect
from requests import NullHandler
from todo_app.data.trello_api import TrelloCard, archive_trello_card, get_trello_cards, get_trello_list_id, move_trello_card, create_trello_card
from todo_app.flask_config import Config
import datetime

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():

    trello_list_ids = {'todo':get_trello_list_id('To Do'),'doing':get_trello_list_id('Doing'),'done':get_trello_list_id('Done')}

    items = get_trello_cards()

    if request.values.get('sort') == '1':
        items.sort(key=lambda x: x.idList)
    elif request.values.get('sort') == '2':
        items.sort(key=lambda x: x.idList, reverse=True)

    return render_template('index.html', items=items,trello_list_ids=trello_list_ids)


@app.route('/new_item', methods=['POST'])
def new_item():
    new_item_title = request.form.get('new_item_title')
    trello_default_list = get_trello_list_id('To Do')
    if request.form.get('due_date'):
        due_date = datetime.datetime.strptime(request.form.get('due_date'), '%d-%m-%Y')
    else:
        due_date = datetime.date.today() + datetime.timedelta(30)
    
    description = ""

    new_card = TrelloCard(0, new_item_title, trello_default_list, due_date, description)
    create_trello_card(new_card)
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
