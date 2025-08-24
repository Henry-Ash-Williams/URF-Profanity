from os import PathLike
import subprocess


class AudioTranscriber:
    def __init__(self, model_size: str = "tiny"):
        self.model_size = model_size

    def __call__(self, input: PathLike, output: PathLike):
        subprocess.run(
            [
                "uvx",
                "whisper-mps",
                "--model-name",
                self.model_size,
                "--file-name",
                input,
                "--output-file-name",
                output,
            ],
            capture_output=True,
            check=True,
        )
