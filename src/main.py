import tempfile
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import track

import argparse
from datetime import datetime
import os

import downloader
import profanity
import shows
from snippet import SnippetGenerator
from transcribe import AudioTranscriber

console = Console()

INFO = "[[b green]*[/b green]]"
ERROR = "[[b red]![/b red]]"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate profanity reports for shows on URF",
        epilog="GWYG does not, has not, and will never exist.",
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Where to save profanity reports and audio snippets",
        required=True,
    )

    parser.add_argument(
        "-n",
        "--name",
        help="Name of the URF show",
        required=True,
    )

    parser.add_argument(
        "-s",
        "--start",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d %H:%M:%S"),
        default=datetime(2025, 1, 1, 0),
        help="Start timestamp in format YYYY-MM-DD HH:MM:SS, defaults to 2025-01-01 00:00:00",
    )

    parser.add_argument(
        "-e",
        "--end",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d %H:%M:%S"),
        default=datetime(2026, 1, 1, 0),
        help="End timestamp in format YYYY-MM-DD HH:MM:SS, defaults to 2026-01-01 00:00:00",
    )

    parser.add_argument(
        "-c",
        "--credentials",
        default="./.env",
        help="Path to `.env` file containing URF archive credentials",
    )

    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="tiny",
        choices=["tiny", "base", "small", "medium", "large", "turbo"],
        help="Size of the whisper model, defaults to 'tiny'",
    )

    parser.add_argument(
        "--save-snippets",
        default=False,
        action="store_true",
        help="Save profanity snippets",
    )
    parser.add_argument(
        "--save-show", default=False, action="store_true", help="Save the show"
    )
    parser.add_argument(
        "--save-transcript",
        default=False,
        action="store_true",
        help="Save the full transcript",
    )
    parser.add_argument(
        "--offset", default=1000, help="Offset amount for snippets", type=int
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    load_dotenv(args.credentials)

    try:
        show_info = shows.Shows()
        show_times = show_info.get_show_times(args.name, args.start, args.end)
    except ValueError:
        console.log(f"{ERROR}: Could not find {args.name} in the timetable")
        exit()
    except Exception as e:
        console.log(f"{ERROR}: Something else went wrong, {e}")
        exit()

    os.makedirs(args.output, exist_ok=True)

    show_downloader = downloader.ShowDownloader(
        username=os.environ["URF_ARCHIVE_USERNAME"],
        password=os.environ["URF_ARCHIVE_PASSWORD"],
    )
    audio_transcriber = AudioTranscriber(args.model)
    profanity_finder = profanity.ProfanityFinder()

    show_name_formatted = f"{args.name.lower().replace(' ', '-')}.mp3"

    for time in track(show_times, console=console):
        show_dir = os.path.join(args.output, time.strftime("%Y-%m-%d_%H:%M:%S"))
        console.log(f"{INFO} Downloading {args.name}, date: {time}")

        with tempfile.TemporaryDirectory() as tmpdir:
            os.makedirs(show_dir, exist_ok=True)
            if args.save_show:
                show_file = os.path.join(show_dir, show_name_formatted)
                console.log(f"{INFO} Saving show to {show_file}")
            else:
                show_file = os.path.join(tmpdir, show_name_formatted)

            try:
                show_downloader.download(time, show_file)
                console.log(f"{INFO} Download complete, generating transcript...")
            except Exception as e:
                console.log(
                    f"{ERROR} Unable to download {show_downloader.generate_url(time)}: {e}"
                )
                os.rmdir(show_dir)
                continue

            if args.save_transcript:
                transcript_file = os.path.join(show_dir, "transcription.json")
                console.log(f"{INFO} Saving transcript to {transcript_file}")
            else:
                transcript_file = os.path.join(tmpdir, "transcription.json")

            audio_transcriber(show_file, transcript_file)
            console.log(f"{INFO} Audio transcribed, identifying profanity")
            profanity_report_path = os.path.join(
                show_dir, show_name_formatted.replace(".mp3", "-profanity-report.csv")
            )

            swears = profanity_finder.identify_profanity(transcript_file)
            console.log(f"{INFO} Profanity report saved to {profanity_report_path}")
            swears.to_csv(profanity_report_path)

            if args.save_snippets:
                snippet_path = os.path.join(show_dir, "snippets")
                os.makedirs(snippet_path, exist_ok=True)
                console.log(f"{INFO} Saving audio snippets to {snippet_path}")
                snippet_generator = SnippetGenerator(show_file, swears, args.offset)
                snippet_generator.extract_snippets(snippet_path)
