It a simple django application showing implementation of restframework and order system

Note:
    - in this project the default database is sqlite and if we need to use other database the we need to install dependency package and change settings.py file
    - we cannot use html form because array is not supported so, please use raw data with json format

For running the application following steps need to be followed
1) install all the packages from requirements.txt (pip install -r requirements.txt)
2) run following command for creating table schema (python manage.py makemigrations)
3) run following command for creating table in database (python manage.py migrate)
4) create super user with the command : python manage.py createsuperuser
5) run application with command : python manage.py runserver 0.0.0.0:port
6) now with the help of super user we can create new users and add orders for them
7) we can use default django restframework templates and form's for testing the api and sample is also attached to the folder sample 