# How to install and run Django on Ubuntu 20.04
1. sudo apt update
2. sudo apt install pip3
3. pip3 install django
4. python3 -m django startproject <project_name>
5. cd <project_name>
6. sudo vim <project_name>/settings.py
7. Add your IP to ALLOWED_HOST. ex. ALLOWED_HOST = ['IP']
8. python3 manage.py runserver