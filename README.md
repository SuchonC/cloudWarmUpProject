# How to install and run Django on Ubuntu 20.04
1. sudo apt update
2. sudo apt install python3-pip
3. pip3 install django
4. python3 -m django startproject <project_name>
5. cd <project_name>
6. sudo vim <project_name>/settings.py
7. Add your IP to ALLOWED_HOST. ex. ALLOWED_HOST = ['IP']
8. python3 manage.py runserver 0.0.0.0:8000

# How to create permanent environment variables
1. sudo vim /etc/profile.d/<new-env>.sh
2. add export <variable_name>=<value> one per line
3. source /etc/profile