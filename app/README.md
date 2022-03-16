# Django Social Media With RestApi using DRF and JWT authentication

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/oldcorvus/social-media.git
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```


Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd app 
(env)$ python manage.py runserver --settings=socialMedia.settings.test

```
And navigate to `http://127.0.0.1:8000/`.


## Walkthrough

Before you interact with the application, go to settings and set up
secret key.


## Tests

To run the tests, `cd` into the directory where `manage.py` is:
```sh
(env)$ python manage.py test --settings=socialMedia.settings.test

```
## API Docs 
  navigate to `http://127.0.0.1:8000/swagger/`
  
## Features
 rest api using drf
 jwt authentications
 ajax scrolling
 
