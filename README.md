# Feed Manager Web Application

This web application is developed using Django, a high-level Python Web framework. It uses `Python 3.8`, `Django 3.0.6`, `Django REST Framework 3.11.0` and `Celery 4.4.2` and SQLite database for development.
This project comprises three main apps:
1. Accounts:
  Used the built-in Django authentication app
2. Feeds:
  This app manages feeds and posts parsed for each Feed and the following APIs:

  
| Endpoint      | HTTP Method  | Result|
| ------------- |:------------:| -----|
| userfeeds        | GET       | Get all the user's feed |
| userfeeds        | POST      | Add a single feed for the authenticated user |
| userfeed/:pk     | DELETE    | Deletes a single user's feed for the authenticated & owner user|
| userposts        | GET       | Get all the posts that the authenticated & owner user has their feed |
| userposts_count  | Get       | Get the count of posts that the authenticated & owner user has their feed |
| userpost/:pk     | Get       | Get a single post that the authenticated & owner user has its feed |
| userpost/:pk     | PUT       | Updates a single post that the authenticated & owner user has its feed |


## Installation via Docker

Before building the image:
1. Change directory to the root project (`feedmanager`).
2. Set up environment variables: Create a `.env` file in the root directory of the project (where `Dockerfile` and `docker-compose.yml` are located).
The contents of `.env` the file should be set as `KEY=VALUE`. 
3. Run the following commands to build the image and run the container respectively:
```shell script
docker-compose build
docker-compose up
```
4. The application will be running at http://127.0.0.1:8000/   