import sys
import asyncio

from collections import namedtuple
from typing import List

from .ffmpeg_util import FFmpegUtils


class FFmpegError(Exception):
    pass


class FFmpeg(FFmpegUtils):
    _File = namedtuple("_File", ["url", "options"])

    def __init__(self, executable="ffmpeg"):
        self._executable = executable
        self._global_options = {}
        self._input_files = []
        self._output_files = []

        self._executed = False
        self._windows = sys.platform == "win32"
        super(FFmpeg, self).__init__()

    def generate_subprocess(self, *args, **kwargs):
        if self._windows:
            from subprocess import CREATE_NEW_PROCESS_GROUP

            kwargs["creationflags"] = CREATE_NEW_PROCESS_GROUP
        return asyncio.create_subprocess_exec(*args, **kwargs)

    def option(self, key, value=None):
        self._global_options[key] = value
        return self

    def input(self, url, options=None, **kwargs):
        if options is None:
            options = {}

        self._input_files.append(FFmpeg._File(url=url, options={**options, **kwargs}))
        return self

    def output(self, url, options=None, **kwargs):
        if options is None:
            options = {}

        self._output_files.append(FFmpeg._File(url=url, options={**options, **kwargs}))
        return self

    async def run_get_progress(self):
        if self._executed:
            raise FFmpegError("AioFFmpeg is already executed")

        arguments = self.options_generator()
        stream = await self.generate_subprocess(
            *arguments, stdin=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        while 1:
            s = await stream.stderr.readline()
            if s:
                o_xu = s.decode("utf8")
                rt = self.parse_progress(o_xu)
                if rt:
                    yield rt

    def options_generator(self) -> List[str]:
        arguments = [self._executable]
        arguments.extend(self.build_options(self._global_options))

        for file in self._input_files:
            arguments.extend(self.build_options(file.options))
            arguments.extend(["-i", file.url])

        for file in self._output_files:
            arguments.extend(self.build_options(file.options))
            arguments.append(file.url)

        return arguments
