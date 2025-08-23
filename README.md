# URF Profanity Identifier

A simple script to identify the use of profanity on [University Radio Falmer](https://www.urfonline.com/) with OpenAI's [whisper](https://github.com/openai/whisper). 

## Install 

1. Clone the repo 

```sh
$ git clone <insert url here>
$ cd <insert repo name here>
```

2. Install dependencies 

```sh
$ uv sync
$ source .venv/bin/activate 
``` 

## Usage 

```
usage: main.py [-h] [--datetime YEAR MONTH DAY HOUR] [-c CREDENTIALS]

options:
  -h, --help            show this help message and exit
  --datetime YEAR MONTH DAY HOUR
                        Specify year, month, day, and hour together. Defaults
                        to the last show broadcasted
  -c CREDENTIALS, --credentials CREDENTIALS
                        Path to the file storing the credentials for accessing
                        the URF archive
```

### Examples 

Generate a report for a show at a specific time: 

```sh
$ python main.py --datetime <year> <month> <day> <hour>
``` 

Or, for the last shows' broadcast: 

```sh
$ python main.py
```

## Requirements 

This script expects a `.env` file in the root of the project, containing the following values for accessing the archive. 

```
URF_ARCHIVE_USERNAME=<urf archive username>
URF_ARCHIVE_PASSWORD=<urf archive password>
```
