"# cuoiky-python" 

"# delete database before running"

pip install django-jet-reboot

"# migrate after that"

python manage.py makemigrations music

python manage.py migrate

"# dump data"

py -Xutf8 manage.py dumpdata music --indent 2 >  seed/music.json 

py -Xutf8 manage.py dumpdata users --indent 2 >  seed/users.json 

"# load data"

py manage.py loaddata  seed/music.json


py manage.py loaddata  seed/users.json


admin
123456
