from flask import Flask
from flask import render_template, request, redirect
from todo_app.data.todo import ToDoCard, ViewModel, get_todo_cards, move_todo_card, create_todo_card
import datetime,pytest

def create_app():

    app = Flask(__name__)

    @app.route('/')
    def index():

        list_ids = {'todo':'todo','doing':'doing','done':'done'}

        items = get_todo_cards()

        item_view_model = ViewModel(items, list_ids)

        todays_date = datetime.datetime.strftime(datetime.date.today(), '%d/%m/%Y')

        if request.values.get('sort') == '1':
            items.sort(key=lambda x: x.due_date)
        elif request.values.get('sort') == '2':
            items.sort(key=lambda x: x.due_date, reverse=True)
        else:
            items.sort(key=lambda x: x.due_date)

        return render_template('index.html', view_model=item_view_model, todays_date=todays_date)


    @app.route('/new_item', methods=['POST'])
    def new_item():
        new_item_title = request.form.get('new_item_title')
        trello_default_list = 'todo'
        if request.form.get('new_item_due'):
            due_date = datetime.datetime.strptime(request.form.get('new_item_due'), '%Y-%m-%d')
        else:
            due_date = datetime.datetime.today() + datetime.timedelta(30)
        
        description = request.form.get('new_item_desc')

        new_card = ToDoCard(0, new_item_title, trello_default_list, due_date, description, datetime.datetime.today())
        create_todo_card(new_card)
        return redirect(request.headers.get('Referer'))

    @app.route('/toggle_status', methods=['POST'])
    def toggle_status():
        card_id = request.form.get('toggle_item_id')
        new_list_id = request.form.get('new_list_id')

        move_todo_card(card_id,new_list_id)

        return redirect(request.headers.get('Referer'))

    if __name__ == '__main__':
        app.run()
    
    return app


