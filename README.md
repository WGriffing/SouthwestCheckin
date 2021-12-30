# SW Checkin

[![Build Status](https://travis-ci.org/pyro2927/SouthwestCheckin.svg?branch=master)](https://travis-ci.org/pyro2927/SouthwestCheckin)
[![Maintainability](https://api.codeclimate.com/v1/badges/aa1c955dfcba58a7352f/maintainability)](https://codeclimate.com/github/pyro2927/SouthwestCheckin/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/aa1c955dfcba58a7352f/test_coverage)](https://codeclimate.com/github/pyro2927/SouthwestCheckin/test_coverage)
[![Docker Build Status](https://img.shields.io/docker/automated/pyro2927/southwestcheckin.svg?style=flat)](https://hub.docker.com/r/pyro2927/southwestcheckin)
[![Docker Image Size](https://images.microbadger.com/badges/image/pyro2927/southwestcheckin.svg)](https://microbadger.com/images/pyro2927/southwestcheckin)

![](http://www.southwest-heart.com/img/heart/heart_1.jpg)

This python script checks your flight reservation with Southwest and then checks you in at exactly 24 hours before your flight. Queue up the script and it will `sleep` until the earliest possible check-in time.

## Contributors

[![](https://sourcerer.io/fame/pyro2927/pyro2927/SouthwestCheckin/images/0)](https://sourcerer.io/fame/pyro2927/pyro2927/SouthwestCheckin/links/0)[![](https://sourcerer.io/fame/pyro2927/pyro2927/SouthwestCheckin/images/1)](https://sourcerer.io/fame/pyro2927/pyro2927/SouthwestCheckin/links/1)[![](https://sourcerer.io/fame/pyro2927/pyro2927/SouthwestCheckin/images/2)](https://sourcerer.io/fame/pyro2927/pyro2927/SouthwestCheckin/links/2)[![](https://sourcerer.io/fame/pyro2927/pyro2927/SouthwestCheckin/images/3)](https://sourcerer.io/fame/pyro2927/pyro2927/SouthwestCheckin/links/3)[![](https://sourcerer.io/fame/pyro2927/pyro2927/SouthwestCheckin/images/4)](https://sourcerer.io/fame/pyro2927/pyro2927/SouthwestCheckin/links/4)[![](https://sourcerer.io/fame/pyro2927/pyro2927/SouthwestCheckin/images/5)](https://sourcerer.io/fame/pyro2927/pyro2927/SouthwestCheckin/links/5)[![](https://sourcerer.io/fame/pyro2927/pyro2927/SouthwestCheckin/images/6)](https://sourcerer.io/fame/pyro2927/pyro2927/SouthwestCheckin/links/6)[![](https://sourcerer.io/fame/pyro2927/pyro2927/SouthwestCheckin/images/7)](https://sourcerer.io/fame/pyro2927/pyro2927/SouthwestCheckin/links/7)

## Requirements

This script can either be ran directly on your host or within Docker.

### Host

- Python (should work with 2.x or 3.x thanks to @ratabora)
- [pip](https://pypi.python.org/pypi/pip)

### Docker

- Docker (tested with 1.12.6)

## Setup

### Host

#### Install Base Package Requirements

```bash
$ pip install virtualenv
$ python -m virtualenv venv
& source venv/bin/activate
(venv)$ pip install -r requirements.txt
```

### southwest-headers setup

1. Clone https://github.com/WGriffing/southwest-headers in parallel with this repo, you should have 2 folders in the same parent dir: `SouthwestCheckin` and `southwest-headers`.
1. Checkout the `develop` branch in the `southwest-headers` repo.
1. Follow the instructions in https://github.com/WGriffing/southwest-headers/blob/develop/README.md to setup the cronjob that will populate the contents of `../southwest-headers/southwest_headers.json` that this script depends on.

#### Usage (Single)

```bash
(venv)$ python checkin.py CONFIRMATION_NUMBER FIRST_NAME LAST_NAME
```

#### Usage (Multiple)

The reservation details are passed as a comma-separated list including the confirmation number, first name, and last name for each reservation.

```bash
(venv)$ python checkin.py RESERVATION_LIST
```

where `RESERVATION_LIST` looks like `CONFIRMATION_NUMBER_1,FIRST_NAME_1,LAST_NAME_1,...,CONFIRMATION_NUMBER_N,FIRST_NAME_N,LAST_NAME_N`.

### Docker

#### Build

```bash
$ docker build -t southwestcheckin:latest .
```

#### Usage (Single)

```bash
$ docker run -it southwestcheckin:latest CONFIRMATION_NUMBER FIRST_NAME LAST_NAME
```

#### Usage (Multiple)

```bash
$ docker run -it southwestcheckin:latest RESERVATION_LIST
```

where `RESERVATION_LIST` looks like `CONFIRMATION_NUMBER_1,FIRST_NAME_1,LAST_NAME_1,...,CONFIRMATION_NUMBER_N,FIRST_NAME_N,LAST_NAME_N`.
