from flask import Flask
from flask import render_template, request, redirect, logging
from todo_app.data.todo import ToDoCard, ViewModel, get_todo_cards, move_todo_card, create_todo_card
import datetime, os, requests, json
from flask_login import LoginManager, login_required, UserMixin, login_user, current_user
from oauthlib.oauth2 import WebApplicationClient
from loggly.handlers import HTTPSHandler
from logging import Formatter


login_manager = LoginManager()

@login_manager.unauthorized_handler
def unauthenticated():
    client = WebApplicationClient(os.environ.get('AUTH_CLIENTID'))
    auth_redirect = client.prepare_request_uri(os.getenv('AUTH_REDIRECT_URL'))

    return redirect(auth_redirect)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id
    @property
    def role(self):
        if self.id == 'lachlanpearse-mclaren' or self.id == 'e2e_test':
            return 'writer'
        else:
            return 'reader'

def create_app():
    

    app = Flask(__name__)
    app.secret_key = os.getenv('APP_SECRET')
    app.config['LOG_LEVEL'] = os.getenv('LOG_LEVEL')
    login_manager.init_app(app)
    app.logger.setLevel(app.config['LOG_LEVEL'])

    if app.config['LOGGLY_TOKEN'] is not None:
        handler = HTTPSHandler(f'https://logs-01.loggly.com/inputs/{app.config["LOGGLY_TOKEN"]}/tag/todo-app')
        handler.setFormatter(Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s"))
        app.logger.addHandler(handler)

    
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


        if 'LOGIN_DISABLED' not in app.config:
            if current_user.role == 'writer':
                return render_template('index.html', view_model=item_view_model, todays_date=todays_date)   
            else:
                return render_template('index_ro.html', view_model=item_view_model, todays_date=todays_date)
        else:
            return render_template('index.html', view_model=item_view_model, todays_date=todays_date)



    @app.route('/new_item', methods=['POST'])
    @login_required
    def new_item():
        if 'LOGIN_DISABLED' in app.config or current_user.role == 'writer':
            new_item_title = request.form.get('new_item_title')
            trello_default_list = 'todo'
            if request.form.get('new_item_due'):
                due_date = datetime.datetime.strptime(request.form.get('new_item_due'), '%Y-%m-%d')
            else:
                due_date = datetime.datetime.today() + datetime.timedelta(30)
            
            description = request.form.get('new_item_desc')

            new_card = ToDoCard(0, new_item_title, trello_default_list, due_date, description, datetime.datetime.today())
            create_todo_card(new_card)
            if 'LOGIN_DISABLED' not in app.config:
                app.logger.info(f"New card created by {current_user.id}")
            else:
                app.logger.info(f"New card created by TestUser")
        return redirect(request.headers.get('Referer'))

    @app.route('/toggle_status', methods=['POST'])
    @login_required
    def toggle_status():
        if 'LOGIN_DISABLED' in app.config or current_user.role == 'writer':
            card_id = request.form.get('toggle_item_id')
            new_list_id = request.form.get('new_list_id')

            move_todo_card(card_id,new_list_id)
            if 'LOGIN_DISABLED' not in app.config:
                app.logger.info(F"Card modified by {current_user.id}, Card ID: {card_id}, New List ID: {new_list_id}")
            else:
                app.logger.info(F"Card modified by TestUser, Card ID: {card_id}, New List ID: {new_list_id}")

        return redirect(request.headers.get('Referer'))

    @app.route('/login')
    def login():
        github_code = request.args.get('code')
        client =  WebApplicationClient(os.environ.get('AUTH_CLIENTID'))
        token = client.prepare_token_request(os.environ.get('AUTH_TOKEN_URL'), code=github_code)
        access = requests.post(token[0], headers=token[1], data=token[2], auth=(os.environ.get('AUTH_CLIENTID'), os.environ.get('AUTH_SECRET')))
        client.parse_request_body_response(access.text)
        github_user_request_param = client.add_token(os.environ.get('AUTH_API_URL'))
        user_id = requests.get(github_user_request_param[0], headers=github_user_request_param[1]).json()['login']
        print(user_id)
        
        login_user(User(user_id))
        app.logger.info(f"User {current_user.id} logged in")

        return redirect('/')

    if __name__ == '__main__':
        app.run()
    
    return app


