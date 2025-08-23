import os
import json
import requests
import tempfile
import argparse
import warnings
import datetime
import subprocess
from typing import Literal

import dotenv
import pandas as pd
from rich.console import Console
from better_profanity import profanity

warnings.filterwarnings("ignore")

profanity.load_censor_words()
console = Console()

ERROR = "[[red]![/red]]"
INFO = "[[green]*[/green]]"


def clip(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def format_url(time):
    return f"https://archive.urfonline.com/{time.year}/{time.month:02}/{time.day:02}/{time.hour:02}.mp3"


def do_extraction(
    input,
    output,
    size: Literal["tiny", "base", "small", "medium", "large", "turbo"] = "tiny",
):
    proc = subprocess.run(
        [
            "uvx",
            "whisper-mps",
            "--model-name",
            size,
            "--file-name",
            input,
            "--output-file-name",
            output,
        ],
        capture_output=True,
    )


def download_show(url, output):
    res = requests.get(
        url, auth=(creds["URF_ARCHIVE_USERNAME"], creds["URF_ARCHIVE_PASSWORD"])
    )

    if not res.ok:
        raise FileNotFoundError("Show not found")

    with open(output, "wb") as f:
        f.write(res.content)


def find_potential_profanity(time):
    with tempfile.TemporaryDirectory() as tdir, console.status(
        "Identifying potential profanity"
    ):
        url = format_url(time)
        audio_output = os.path.join(tdir, "audio.mp3")
        console.log(f"{INFO} Downloading show from {url}")
        try:
            download_show(url, audio_output)
        except FileNotFoundError as e:
            console.log(f"{ERROR} Show not found")
            raise e
        except Exception as e:
            console.log(f"{ERROR} Failed to download the show: {e}")
            raise e

        console.log(f"{INFO} Done, audio saved to {audio_output}")

        transcript_output = os.path.join(tdir, "output.json")
        console.log(f"{INFO} Generating transcript")
        try:
            do_extraction(audio_output, transcript_output)
        except Exception as e:
            console.log(f"{ERROR} Failed to generate transcript: {e}")
            raise e

        console.log(f"{INFO} Done, transcript saved to {transcript_output}")

        console.log(f"{INFO} Formatting data")
        with open(transcript_output, "r") as f:
            transcript_output = json.load(f)

        swears = []
        for segment in transcript_output["segments"]:
            start = segment["start"]
            end = segment["end"]
            if profanity.contains_profanity(segment["text"]):
                swears.append({"start": start, "end": end, "content": segment["text"]})

        console.log(f"{INFO} Done")
        return pd.DataFrame(swears)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--datetime",
        nargs=4,
        metavar=("YEAR", "MONTH", "DAY", "HOUR"),
        type=int,
        help="Specify year, month, day, and hour together. Defaults to the last show broadcasted",
    )
    parser.add_argument(
        "-c",
        "--credentials",
        default=".env",
        type=str,
        help="Path to the file storing the credentials for accessing the URF archive",
    )

    args = parser.parse_args()
    creds = dotenv.dotenv_values(args.credentials)

    if args.datetime is None:
        dt = datetime.datetime.now()
        dt -= datetime.timedelta(hours=1)
    else:
        year, month, day, hour = args.datetime
        dt = datetime.datetime(year, month, day, hour)

    try:
        df = find_potential_profanity(dt)
        formatted = dt.strftime("%Y-%m-%d-%H-profanity-report.csv")
        df.to_csv(formatted)
        console.log(f"{INFO} Report saved to {formatted}")
    except Exception as e:
        console.log(f"{ERROR} Failed to generate report: {e}")
