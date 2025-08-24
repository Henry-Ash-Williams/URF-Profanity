import pandas as pd
from pydub import AudioSegment

import os
from os import PathLike


class SnippetGenerator:
    def __init__(
        self, audio_path: PathLike, swears: pd.DataFrame, offset_ms: int = 1000
    ):
        self.audio_path = audio_path
        self.swears = swears
        self.offset_ms = offset_ms

    def extract_snippets(self, output: PathLike):
        audio = AudioSegment.from_file(self.audio_path)
        duration_ms = len(audio)

        for i, row in enumerate(self.swears.itertuples()):
            start_ms = max(0, (row.start * 1000) - self.offset_ms)
            end_ms = min(duration_ms, (row.end * 1000) + self.offset_ms)

            snippet = audio[start_ms:end_ms]
            snippet.export(os.path.join(output, f"snippet-{i}.wav"))
