# Feed Manager Web Application

This web application is developed using Django, a high-level Python Web framework. This project utilizes `Python 3.8`, `Django 3.1.8`, `Django REST Framework 3.11.2`, `Celery 4.4.5`, `Celery Beat 2.0.0` and SQLite database for development.
This project works as a backend service for an RSS scraper and feed reader application. The application saves RSS feeds to a database and lets the user view and manage his feeds via RESTful APIs. Authentication is done using a **token-based** HTTP Authentication scheme. 
It comprises the following components:
1. Accounts App:
    A customized the Django authentication user model that registers and authenticates the user using email (instead of username) and password.
2. Feeds App:
    This app manages feeds and posts parsed for each Feed. The user can have multiple feeds, add bookmark/ favourite to posts and comment on a post.
3. Celery:
    The feed manager updates the feeds in the background periodically. Feed items (posts) are read asynchronously, every five minutes. Celery Beat is used as the scheduler, Celery as the task queue and RabbitMQ as the broker.
    In order to start the services related to this feature, run the following commands:
```shell script
rabbitmq-server   # start rabbitmq service
celery -A feedmanager worker -l info
celery -A feedmanager beat -l info
``` 
4. RESTful APIs: The following APIs expose all the necessary functionality to register, login, view and manage all feeds registered by the user:

| Endpoint                          | HTTP Method   | Result     |
| -------------------------------   |:-------------:| -----------|
| /api/accounts/v1/register/        | POST      | Register a new user with email and password and return the user's token  
| /api/accounts/v1/login/           | POST      | Login with credentials (email & password) and get user's token
| /api/feeds/v1/userfeeds/          | GET       | Get all the user's feeds |
| /api/feeds/v1/userfeeds/          | POST      | Add a single feed for the authenticated user |
| /api/feeds/v1/userfeed/:pk/       | GET       | Get a single user's feed for the authenticated & owner user|
| /api/feeds/v1/userfeed/:pk/       | DELETE    | Deletes a single user's feed for the authenticated & owner user|
| /api/feeds/v1/userposts/          | GET       | Get all the posts of all feed that user has registered for |
| /api/feeds/v1/userposts/feed/:pk/ | GET       | Get all the posts of a specific feed that user has registered for |
| /api/feeds/v1/userpost/:pk/       | GET       | Get a single post detail that user has registered its feed |
| /api/feeds/v1/userpost/:pk/       | PUT       | Updates a single post that user has registered its feed |
 
5. Django TestCases and API TestCases

## Installation via Docker

Before building the image:
1. Change directory to the root project (`feedmanager`).
2. Set up environment variables: Create a `.env` file in the root directory of the project (where `Dockerfile` and `docker-compose.yml` are located).
3. Run the following commands to build the images and spin up the containers respectively:
```shell script
docker-compose up --build
```
4. The application will be running at http://127.0.0.1:8000/


