# Pesto

<p align="center" width="100%">
  <img src="logo.png" width="150">
</p>

<p align="center" width="100%">
<a href="https://coveralls.io/github/addy999/Pesto"><img alt="Coverage Status" src="https://coveralls.io/repos/github/addy999/Pesto/badge.svg"></a>
<a href="https://travis-ci.com/addy999/Pesto"><img alt="Build Status" src="https://travis-ci.com/addy999/Pest.svg?branch=main"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://github.com/psf/black/blob/master/LICENSE"><img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg"></a>
<p align="center" width="100%">🚧 Under Development 🚧</p>
</p>

### A lightweight, fun-to-use Python testing framework made to use like the popular JS Jest library.
<br>


## Why?
Coming back to software development after being a front-end engineer opened my eyes on how verbose and anti-user-friendly Python testing really is - in my opinion.

I want to enjoy writing tests as much as I loved them with my front-end stack, so I decided to create a little testing framework to mimic that behavior, while still being a robust testing tool.

## Get Started

The CLI is very similar to PyTest. Simply give the directory of the tests as the first argument (or `./` is used by default.)

**A drag and drop replacement for PyTest**

Pesto looks for test files and functions with `_test` or `test_` in the name.

```bash
pip install pesto
pesto <test-dir>
```

<p align="center" width="100%">
  <img src="terminal.gif">
</p>


## Development
I'm still a novice when it comes to testing, so the capabilities of this library will grow as I grow as a developer


## Todo
### General

- [ ] Add multiprocessing support to run tests in parallel
- [ ] Create github action
- [ ] Add Poetry

### unittest / pytest like functionality:
- [ ] Mocking (integrate unittest.mock)
