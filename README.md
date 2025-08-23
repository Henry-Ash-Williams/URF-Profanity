# URF Profanity Identifier


<p align="center">
  <img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmedia.tenor.com%2F7R0cugwI7k0AAAAC%2Fwatch-your-mouth-watch-your-profanity.gif&f=1&nofb=1&ipt=1d1d3ff67810bcb19216eba0dadc6425e66fa0b241e5329c01cac3df1545cf53" alt-text="watch yo profanity"/>
</p>


A simple script to identify the use of profanity on [University Radio Falmer](https://www.urfonline.com/) with OpenAI's [whisper](https://github.com/openai/whisper). 

## Install 

1. Clone the repo 

```sh
$ git clone https://github.com/Henry-Ash-Williams/URF-Profanity
$ cd URF-profanity
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
