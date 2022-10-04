init: flask --app main.py db init
migrrate: flask --app main.py migrate
release: flask --app main.py db upgrade
web: gunicorn 'main:create_app()'
