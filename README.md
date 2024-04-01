# Instagram Copy
A Django based personal site to help users to share their posts. Users can upload photos and share them with their followers. They can view, comment and like other user's posts by following them, and allow other users to explore own posts by accepting their friend requests.

## Dependancies
###### pip install django
###### pip install django-crispy-forms crispy-bootstrap5
###### pip install pillow

# Running
###### Set Environment Variables from settings.py:

- DJANGO_KEY
- IS_DEBUG
- STATIC_ROOT_PATH
- MEDIA_ROOT_PATH
###### python manage.py makemigrations users world

###### python manage.py migrate

###### python manage.py createsuperuser

###### python manage.py runserver

# Demo
- [Homepage](http://127.0.0.1:8000/)

#### Users:
-    username | password 
-    ----------+----------
-    user2    | user2
-    user1    | user1
-    user3    | user3


