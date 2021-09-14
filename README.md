# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Configuring MongoDB Information

To configure this application to work with MongoDB, you need to update the following variables in the .env file:

    MONGO_DB_CONNECTION: The connection string to your MongoDB account
    MONGO_DB_NAME: The name you'd like to have for your MongoDB for this application

### Test Configuration

To run the unit tests, you will require pytest to be installed. You will also require the chromedriver.exe binary in the root directory for
the end to end tests to work.

You can then run: "poetry run pytest" to execute all the currently defined tests. 

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.tempalate` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). 

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Running the App Within Containers

Assuming Docker is installed already, the application can be started inside Docker containers. There is a three-stage Dockerfile included that allows for a production, development and test environment to be easily run. Follow the steps below to run each environment.

To build each environment's image, run the following commands:

```bash
$ docker build --target production --tag todo-app:prod .
```
```bash
$ docker build --target development --tag todo-app:dev .
```
```bash
$ docker build --target test --tag todo-app:test .
```

To start each environment, run the following commands:

```bash
$ docker run --env-file .env -p 5000:5000 todo-app:prod 
```
```bash
$ docker run --env-file .env -p 5000:5000 --mount type=bind,source=$(pwd)/todo_app,target=/app/todo_app todo-app:dev 
```
```bash
$ docker run --env-file .env --mount type=bind,source=$(pwd)/todo_app,target=/app/todo_app todo-app:test 
```

To start the full development/test suite, you can use docker-compose with the following command:
```bash
$ docker-compose up --build 
```
The test container will monitor for code changes and automatically re-run the test suite.
