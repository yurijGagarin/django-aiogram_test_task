setup:
	pip install -r requirements.txt
run-bot:
	python bot/main.py
run-server:
	python aiogram_django/manage.py runserver
