# Brunch

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Contributing](../CONTRIBUTING.md)

## About <a name = "about"></a>

Accounting system for catering.

Frontend - React \
Backend - Django, Celery \
DBMS - SQLite (just for now), Redis (for cache)


## Getting Started <a name = "getting_started"></a>

### Prerequisites

To run the project, you need to install the Docker desktop

```
Install Docker desktop. 
https://www.docker.com/products/docker-desktop/
```

### Installing

Make sure that you do not have running Redis server. If so, stop it

```
cd branch
```

For initial launch, run:

```
docker-compose up --build
```

To stop the app, just use CTRL+C in the command line.\
For the next launch just use

```
docker-compose up
```
