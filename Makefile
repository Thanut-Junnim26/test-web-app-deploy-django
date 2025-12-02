run:
	python3 manage.py runserver

migrate:
	python3 manage.py migrate

migrations:
	python3 manage.py makemigrations

install:
	pip install -r requirements.txt

test:
	python3 manage.py test
