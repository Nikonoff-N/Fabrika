#Start Django
1. django-admin startproject mysite
2. python manage.py runserver 0:8000
3. python manage.py startapp myapp
4. INSTALLED_APPS = [
    'myapp.apps.MyappConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
5. python manage.py makemigrations
6. python manage.py migrate
7. python manage.py createsuperuser
8. admin.site.register(Question)
9. 
from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

10. python manage.py rqworker --with-scheduler