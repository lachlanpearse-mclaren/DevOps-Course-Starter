from flask import Flask
from flask import render_template, request, redirect
from todo_app.data.todo import ToDoCard, ViewModel, get_todo_cards, move_todo_card, create_todo_card
import datetime, os, requests, json
from flask_login import LoginManager, login_required, UserMixin, login_user, current_user
from oauthlib.oauth2 import WebApplicationClient

login_manager = LoginManager()

@login_manager.unauthorized_handler
def unauthenticated():
    client = WebApplicationClient(os.environ.get('GITHUB_CLIENTID'))
    auth_redirect = client.prepare_request_uri('https://github.com/login/oauth/authorize')

    return redirect(auth_redirect)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id
    @property
    def role(self):
        if self.id == 'lachlanpearse-mclaren':
            return 'writer'
        else:
            return 'reader'

def create_app():
    

    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    login_manager.init_app(app)

    
    @app.route('/')
    @login_required
    def index():

        items = get_todo_cards()

        item_view_model = ViewModel(items)

        todays_date = datetime.datetime.strftime(datetime.date.today(), '%d/%m/%Y')

        if request.values.get('sort') == '1':
            items.sort(key=lambda x: x.due_date, reverse=True)
        else:
            items.sort(key=lambda x: x.due_date)


        if hasattr(current_user, 'role'):
            if current_user.role == 'writer':
                return render_template('index.html', view_model=item_view_model, todays_date=todays_date)   
            else:
                return render_template('index_ro.html', view_model=item_view_model, todays_date=todays_date)
        else:
            return render_template('index.html', view_model=item_view_model, todays_date=todays_date)



    @app.route('/new_item', methods=['POST'])
    @login_required
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
    @login_required
    def toggle_status():
        card_id = request.form.get('toggle_item_id')
        new_list_id = request.form.get('new_list_id')

        move_todo_card(card_id,new_list_id)

        return redirect(request.headers.get('Referer'))

    @app.route('/login')
    def login():
        github_code = request.args.get('code')
        client =  WebApplicationClient(os.environ.get('GITHUB_CLIENTID'))
        token = client.prepare_token_request('https://github.com/login/oauth/access_token', code=github_code)
        access = requests.post(token[0], headers=token[1], data=token[2], auth=(os.environ.get('GITHUB_CLIENTID'), os.environ.get('GITHUB_SECRET')))
        client.parse_request_body_response(access.text)
        github_user_request_param = client.add_token('https://api.github.com/user')
        user_id = requests.get(github_user_request_param[0], headers=github_user_request_param[1]).json()['login']
        print(user_id)
        
        login_user(User(user_id))

        return redirect('/')

    if __name__ == '__main__':
        app.run()
    
    return app


