| [![Coverage Status](https://coveralls.io/repos/github/dmaish/HelloAPI/badge.svg?branch=tests)](https://coveralls.io/github/dmaish/HelloAPI?branch=tests)|

[![Build Status](https://travis-ci.org/dmaish/HelloAPI.svg?branch=tests)](https://travis-ci.org/dmaish/HelloAPI)|

[![Maintainability](https://api.codeclimate.com/v1/badges/3e91688355b14079fbc5/maintainability)](https://codeclimate.com/github/dmaish/HelloAPI/maintainability)|

## HelloAPI
HelloApi is a library book borrowing and restocking api.It helps an admin user add, edit or delete a book.Helps a user checkout their profile and borrow books

## Endpoint functionality

| Endpoints           | Functionality     | method |
| -------------       |:-------------:    | -----: |
| /api/books          | add a new book    | POST   |
| /api/book/id        | get specific book | GET    |
| /api/book/id        | edit specific book| PUT    |
| /api/auth/register  | user registration | POST   |
| /api/auth/login     | user login        | POST   |
| /api/users/id       | borrow a book     | POST   |
