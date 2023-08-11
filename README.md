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

    Test user:
    
    login: Tomzerw              
    password: Tompassword123q!

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
python manage.py createsuperuser
python manage.py collectstatic
python manage.py runserver

You should create .env:
    - DJANGO_SECRET_KEY
    - DJANGO_DEBUG
    - DATABASE_URL
```

## Demo
![Website Interface](demo.png)

## Features
  - In the task list, you can search for tasks by name and sort them by deadline, status, and priority.
  - I've added tags to tasks. You can view the usage of each tag on the tag list. Additionally, you can see how many tasks are associated with each tag in the tag details section. You can also sort tags by the quantity of tasks they're linked to and search for tags by their names.
  - In the task type list, you'll find the quantity of tasks for each task type. Further details about these tasks are available in the task type details section. You can sort task types by the quantity of tasks they contain and search for specific task types by their names.
  - For positions listed, the number of employees assigned to each position is provided. You can search for positions by name and sort them based on the quantity of employees in each position.
  - When looking at the employee list, you can search for employees by their usernames. In the employee details section, you can see the number of tasks an employee has completed, failed, and currently has in progress. Additionally, you'll find some extra information about the employee.
  - All lists support pagination for easier navigation.
