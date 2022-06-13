export FLASK_APP=neat
export FLASK_ENV=development
flask init-db
flask run

celery -A neat.src.service.celeryApp worker -l INFO -P eventlet