import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobportal.settings')
app = Celery('jobportal')
app.config_from_object('django.conf:settings', namespace='CELERY')
 # celery needs configuration, instead of seperate config file, we put it all in setting.py,easier to manage
 
app.autodiscover_tasks() 
# we will create task in task.py files, inside each app, this line finds them automatically
