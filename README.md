# zerodha

Step 1:
Download Files:

$ git clone https://github.com/rdhar8502/zerodha.git

Step 2:
setup enviaroment

$ pip install virtualenv 
$ virtualenv venv
$ source venv/Scripts/activate

step 3:
Download requirements

$ cd zerodha
$ pip install -r requirements.txt

step 4:
Download Redis

paste this link on browser
https://github.com/MicrosoftArchive/redis/releases/download/win-3.2.100/Redis-x64-3.2.100.msi

Install it!

locate : C:\Program Files\Redis
start redis-cli.exe

step 5:
create db and migrate

$ python manage.py makemigrations
$ python manage.py migrate

step 6:
create superuser

$ python manage.py createsuperuser
<fill all your details as needed>

step 7:
Run Server App:

$ python manage.py runserver

step 8:
setup scheduler through admin

Login to:
http://127.0.0.1:8000/admin/

locate "PERIODIC TASKS" > "Periodic tasks"
click add button and then update records


!DONE!
