# Bank Manager API

URLs:
* Access admin panel using /admin url
* View api documents using /doc url (login using the admin account)

Tasks Tips:
* For adding daily %10 profit, a task will run every night at 00:30 (check the users/tasks.py)
* For sms sending check logs from celery-worker container

Permissions:
* Only superuser can create the user account (CustomUser model).
* Only superuser and a manager user(a user which have a branch) can create accounts (Account model).
* Only the superuser and the branch manager of the user's account can delete the account
* Only superuser can create or edit a branch
* Branch manager can only create a transaction using admin page
* Each branch manager can only see his/her branch and transactions of his/her branch

#### Run the project
First create a local_settings.py file in BankManager app
```bash
cp BankManager/.local_settings_template.py BankManager/local_settings.py
```
The content of this file does not need to change if you want to run the project using docker

create a file called env
```bash
cp .env-default env
```
If you want to change the configs of docker files, make sure the variables of the env file is changed too.


If you want to run the project in the debug model adds DEBUG=1 variable in the env file.

Build and run the project using following command:
```bash
docker-compose up -d --build
```

Then run the following commands
```bash
# apply the migrations
docker-compose exec web python manage.py migrate --noinput

# creates the superuser
docker-compose exec web python manage.py createsuperuser
```

Access project using [http://127.0.0.1:1337/admin/](http://localhost:1337/admin/)