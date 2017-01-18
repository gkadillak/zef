# Sprintly Retrospective Data

## Introduction

This script is a tool for extracting data from the Sprint.ly API

## Usage

1. (from project root) Setup a virtualenv

```
$ virtualenv venv
$ source ./venv/bin/activate
```
 
2. Install requirements
 
```
$ pip install -r requirements.txt
```

3. Run the script, and answer prompts with data (email, API token, tag to query)

```
$ python main.py
```

4. Look at the results

```
$ open planning.txt
```

## License

[Beerware](https://en.wikipedia.org/wiki/Beerware)

/*
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * gkadillak wrote this file.  As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return.   Garrett Kadillak
 * ----------------------------------------------------------------------------
 */