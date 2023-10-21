# Event Management System - Backend

This repository contains the backend codebase for an Event Management System, built using Django.

## Architecture

The backend is developed in Python using the Django web framework. It follows the MVC (Model-View-Controller) pattern for structuring the application. The models define the data structure, views handle the logic and rendering, and templates manage the presentation layer.

## Setup Instructions

### Prerequisites
- Python 3.x
- Django 4.2.6
- Other dependencies as listed in requirements.txt

### Installation Steps

1. Clone the repository using the following command:

git clone https://github.com/Amits212/Event-management-

cd your-repo

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver

Access the application at http://127.0.0.1:8000/calendar/

Used efficient database indexing for frequently accessed data.

Postman API documentation detailing endpoint are provided.

Unit tests have been written to ensure the stability of the application.
