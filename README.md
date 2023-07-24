# Task Manager Project

Django pet-project for managing tasks, implemented in simple way without permissions and with django built-in login system 

## Functionality
  - Position (CRUD)
  - Employee (CRUD)
  - Task (CRUD)
  - TaskType (CRUD)
  - Tag (CRUD)

## Check it out!
[Task manager project deployed to Render](https://task-manager-stsc.onrender.com/tasks/)

## Installation

Python3 must be already installed

```shell
git clone https://github.com/AntonShpakovych/task-manager-service/tree/develop
сd task-manager-service
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py runserver

You should create .env:
    - DJANGO_SECRET_KEY
    - DJANGO_DEBUG
    - DATABASE_URL
```
## Test user

login: Tomzerw              
password: Tompassword123q!

## Demo
![Website Interface](demo.png)
