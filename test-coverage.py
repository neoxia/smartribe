from subprocess import call


call("coverage run --source='./api/views' manage.py test", shell=True)
call("coverage report", shell=True)
