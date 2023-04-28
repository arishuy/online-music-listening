"# cuoiky-python" 

"# delete database before running"
"# migrate after that"

python manage.py makemigrations music

python manage.py migrate

"# load data"
py manage.py loaddata  seed/music.json


py manage.py loaddata  seed/users.json


admin
123456
