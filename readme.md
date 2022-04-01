# Realmusic

## Requirements

To run this project you must install Docker and Docker-compose
- [Install Docker](https://docs.docker.com/engine/install/)
- [Install Docker-compose](https://docs.docker.com/compose/install/)

## Installation
Clone the project
```sh
  git clone https://github.com/mam3d/Realmusic.git
```
create .env file with following environment variables
- SECRET_KEY
- DATABASE_NAME
- DATABASE_USER
- DATABASE_PASSWORD

Run project
```sh
  docker-compose up -d
```
You have 2 containers running
- realmusic
- realmusic_db

Create super user with realmusic container to access Django's Admin panel
```sh
  docker-compose run realmusic python manage.py createsuper user
```
[Admin panel endpoint](http://127.0.0.1:8000/admin)

Now You are ready to use realmusic
