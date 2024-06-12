# Real Estate API

This is a Django-based real estate API that provides endpoints for managing agents, properties, images, reviews, favorites, and users. The API supports JWT authentication and includes various additional functionalities such as searching, filtering, and favorite listing.

## Features

- **Agents**: Manage real estate agents.
- **Properties**: Manage real estate properties.
- **Images**: Manage images associated with properties.
- **Reviews**: Manage reviews for properties.
- **Favorites**: Manage users' favorite properties.
- **Users**: Manage user information and perform operations like searching by email,getting self details, etc.

## Endpoints

- `/agents/`
- `/properties/`
- `/images/`
- `/reviews/`
- `/favorites/`
- `/users/`

```
You can view all endpoints in main page i.e localhost:8000
```

## Installation

### Prerequisites

- Python 3.10+
- Django 5.0+
- Django REST framework
- PostgreSQL (or any preferred database, But I have used postgres in this project)

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/pokhrelgopal/RealEstate-API
   ```

2. **Create a virtual environment and activate it:**

   ```bash
   python3 -m venv venv
   . venv/Scripts/activate

   # This is for windows. Command may differ in other OS
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**

   Configure your database settings in `settings.py`. Example for PostgreSQL:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

   ```bash
     I have kept .env file as public so you can look how i have my environment variables
   ```

5. **Apply migrations:**

   ```bash
   python manage.py migrate
   ```

6. **Create a superuser:**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the server:**

   ```bash
   python manage.py runserver
   ```

## Usage

### Authentication

This API uses JWT authentication to perform different requests. You can obtain a token by sending a POST request to `/api/user/token/` with your username and password:

```bash
curl -X POST -d "email=<email>&password=<password>" http://127.0.0.1:8000/api/v1/user/token/
```
