from flask import Flask
from flask import render_template, request, redirect
from todo_app.data.trello_api import TrelloCard, ViewModel, archive_trello_card, get_trello_cards, get_trello_list_id, move_trello_card, create_trello_card
import datetime,pytest

def create_app():

    app = Flask(__name__)

    @app.route('/')
    def index():

        trello_list_ids = {'todo':get_trello_list_id('To Do'),'doing':get_trello_list_id('Doing'),'done':get_trello_list_id('Done')}

        items = get_trello_cards()

        item_view_model = ViewModel(items, trello_list_ids)

        todays_date = datetime.datetime.strftime(datetime.date.today(), '%d/%m/%Y')

        if request.values.get('sort') == '1':
            items.sort(key=lambda x: x.idList)
        elif request.values.get('sort') == '2':
            items.sort(key=lambda x: x.idList, reverse=True)

        return render_template('index.html', view_model=item_view_model, todays_date=todays_date)


    @app.route('/new_item', methods=['POST'])
    def new_item():
        new_item_title = request.form.get('new_item_title')
        trello_default_list = get_trello_list_id('To Do')
        if request.form.get('new_item_due'):
            due_date = datetime.datetime.strptime(request.form.get('new_item_due'), '%Y-%m-%d')
        else:
            due_date = datetime.date.today() + datetime.timedelta(30)
        
        description = request.form.get('new_item_desc')

        new_card = TrelloCard(0, new_item_title, trello_default_list, due_date, description, datetime.datetime.today())
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
    
    return app


