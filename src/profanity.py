import json
from os import PathLike
import pandas as pd
from better_profanity import profanity


class ProfanityFinder:
    def __init__(self):
        profanity.load_censor_words()

    def identify_profanity(self, transcript: PathLike):
        with open(transcript, "r") as f:
            transcript = json.load(f)

        swears = []
        for segment in transcript["segments"]:
            start = segment["start"]
            end = segment["end"]
            if profanity.contains_profanity(segment["text"]):
                swears.append({"start": start, "end": end, "content": segment["text"]})

        return pd.DataFrame(swears)
