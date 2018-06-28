[![Coverage Status](https://coveralls.io/repos/github/dmaish/HelloAPI/badge.svg?branch=tests)](https://coveralls.io/github/dmaish/HelloAPI?branch=tests)
[![Build Status](https://travis-ci.org/dmaish/HelloAPI.svg?branch=tests)](https://travis-ci.org/dmaish/HelloAPI)
[![Maintainability](https://api.codeclimate.com/v1/badges/3e91688355b14079fbc5/maintainability)](https://codeclimate.com/github/dmaish/HelloAPI/maintainability)

## HelloAPI
HelloApi is a library book borrowing and restocking api.It helps an admin user add, edit or delete a book.Helps a user checkout their profile and borrow books

## API documentation
https://hellobooks6.docs.apiary.io/#reference

## Endpoint functionality

| Endpoints                        | Functionality                    | method |
| -------------                    |:-------------:                   | -----: |
| /api/books                       | add a new book                   | POST   |
| /api/book/id                     | get specific book                | GET    |
| /api/book/id                     | edit specific book               | PUT    |
| /api/auth/register               | user registration                | POST   |
| /api/auth/login                  | user login                       | POST   |
| /api/users/id                    | borrow a book                    | POST   |
|/api/users/books                  |Get User borrowing history        |GET
|/api/users/books?returned=false   |Get books not yet been returned   |GET 
|/api/auth/logout                  |Logs out a user                   |POST
|/api/auth/reset-password          |Password reset                    |POST


## Installing and running the application
1. clone the repo at : https://github.com/dmaish/HelloAPI/tree/develop
2. Install virtualenv : pip install virtualenv
3. CD into the application folder
3. Make a virtual environment : virtualenv you-env
4. Activate the virtual environment
5. Install the requirements: pip install -r requirements.txt
6. Run the application: flask run

## Running the tests
1. Cd into the tests folder : cd tests
2. Run the tests: nosetest --with coverage

## Designs Link
https://dmaish.github.io/HelloBooks/index.html

## Deployment Link
https://quiet-waters-54661.herokuapp.com/

## Made with
1. Flask
2. Postgresql
3. Heroku

## contributors
1. Daniel Maina
2. Andela Kenya
