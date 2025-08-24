import pandas as pd
from pydub import AudioSegment

import os
from os import PathLike


class SnippetGenerator:
    def __init__(self, audio_path: PathLike, swears: pd.DataFrame):
        self.audio_path = audio_path
        self.swears = swears

    def extract_snippets(self, output: PathLike):
        audio = AudioSegment.from_file(self.audio_path)

        for i, row in enumerate(self.swears.itertuples()):
            start_ms = row.start * 1000
            end_ms = row.end * 1000

            snippet = audio[start_ms:end_ms]
            snippet.export(os.path.join(output, f"snippet-{i}.wav"))
