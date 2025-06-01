# osu!skrungly API service

a little REST API built using flask. it provides an interface for frontend services (like the [website](https://github.com/skrungly/osu-skrungly-web) and [discord bot](https://github.com/skrungly/osu-skrungly-discord)) so they can interact with the [bancho.py](https://github.com/skrungly/bancho.py) database, with some specialised endpoints for fetching score screens, etc.

## setup and deployment

it is assumed that you have access to a running instance of [bancho.py](https://github.com/skrungly/bancho.py) in order to deploy this service.

start by cloning this repository and making a copy of `.env.example` with the necessary config edits:

```sh
$ cp .env.example .env
$ nano .env  # use any editor you like!
```

in particular, the `SECRET_KEY` variable should be generated and stored securely. the flask documentations recommends the following command for generating one:

```sh
$ python -c 'import secrets; print(secrets.token_hex())'
```

then launching the service is as simple as

```sh
$ docker compose up --build -d
```

## running tests

no separate configuration or bancho instance is needed to run the tests. just clone the repository and run:

```sh
$ docker compose -f docker-compose.test.yml up --build --exit-code-from flask
```
