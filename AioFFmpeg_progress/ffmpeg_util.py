import re
from .interface import Progress


class FFmpegUtils:
    def __init__(self) -> None:
        """Initialization"""
        self.progress_pattern = re.compile(
            r"(frame|fps|size|time|bitrate|speed)\s*\=\s*(\S+)"
        )

    @staticmethod
    def build_options(options):
        arguments = []

        for key, value in options.items():
            if key.startswith("-"):
                key = key[1:]

            argument = ["-{key}".format(key=key)]
            if value is not None:
                argument.append(str(value))
            arguments.extend(argument)

        return arguments

    def parse_progress(self, line):
        items = {
            key: value
            for key, value in self.progress_pattern.findall(
                line.replace("kB", "").replace("kbits/s", "").replace("x", "")
            )
        }
        if not items:
            return None
        return Progress(**items)
