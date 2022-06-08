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
- EMAIL_HOST_USER
- EMAIL_HOST_PASSWORD

Run project
```sh
  docker-compose up -d
```
You have 4 containers running
- realmusic
- realmusic_db
- redis
- nginx

Create super user with realmusic container to access Django's Admin panel
```sh
  docker-compose exec realmusic python manage.py createsuperuser
```
[Admin panel endpoint](http://127.0.0.1:8000/admin)
[Documantation endpoint](http://127.0.0.1:8000/api/doc)

Now You are ready to use realmusic
