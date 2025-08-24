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
usage: main.py [-h] -o OUTPUT -n NAME [-s START] [-e END] [-c CREDENTIALS]
               [-m {tiny,base,small,medium,large,turbo}] [--save-snippets]
               [--save-show] [--save-transcript] [--offset OFFSET]

Generate profanity reports for shows on URF

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Where to save profanity reports and audio snippets
  -n NAME, --name NAME  Name of the URF show
  -s START, --start START
                        Start timestamp in format YYYY-MM-DD HH:MM:SS,
                        defaults to 2025-01-01 00:00:00
  -e END, --end END     End timestamp in format YYYY-MM-DD HH:MM:SS, defaults
                        to 2026-01-01 00:00:00
  -c CREDENTIALS, --credentials CREDENTIALS
                        Path to `.env` file containing URF archive credentials
  -m {tiny,base,small,medium,large,turbo}, --model {tiny,base,small,medium,large,turbo}
                        Size of the whisper model, defaults to 'tiny'
  --save-snippets       Save profanity snippets
  --save-show           Save the show
  --save-transcript     Save the full transcript
  --offset OFFSET       Offset amount for snippets
```

### Examples 

Generate reports for a show within a certain time range

```sh
$ python src/main.py -n "<Show Name>" -s "2025-01-01 00:00:00" -e "2025-06-01 00:00:00" -o "/path/to/reports"
``` 

## Requirements 

This script expects a `.env` file in the root of the project, containing the following values for accessing the archive. 

```
URF_ARCHIVE_USERNAME=<urf archive username>
URF_ARCHIVE_PASSWORD=<urf archive password>
```
