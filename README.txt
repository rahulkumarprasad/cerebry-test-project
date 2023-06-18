It a simple django application showing implementation of restframework and order system

Note:
    - in this project the default database is sqlite and if we need to use other database the we need to install dependency package and change settings.py file
    - we cannot use html form because array is not supported so, please use raw data with json format
    - Sample data for database sqlite is provided please run the application and test

For running the application following steps need to be followed
1) install all the packages from requirements.txt (pip install -r requirements.txt)
2) run following command for creating table schema (python manage.py makemigrations)
3) run following command for creating table in database (python manage.py migrate)
4) create super user with the command : python manage.py createsuperuser (if sqlite file is used form git hub then follow Already Initalized steps)
5) run application with command : python manage.py runserver 0.0.0.0:port
6) now with the help of super user we can manipulate admin data's

- Already Initalized steps
1) pull from git and install all required packages from requirement.txt
2) two users are present
    - username:admin, password:admin
    - username:rahulkumar, password:rahulk5665
3) login with admin user to manipulate admin data
4) login with rahul user to place order
5) video for the demo is givin in the git sample folder