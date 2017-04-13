web: gunicorn -w 4 wsgi:application
init: python manage.py db upgrade head
seed: python manage.py seed
generate_fake: python manage.py generate_fake