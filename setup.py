from setuptools import setup, find_packages

setup(
    name="AioFFmpeg_progress",
    version="0.0.1",
    description="asynchronous ffmpeg wrapper and ffmpeg Progress",
    url="https://github.com/zeroday0619/AsyncFFmpeg",
    author="zeroday0619 [Euiseo Cha]",
    author_email="zeroday0619@kakao.com",
    install_requires=["pydantic"],
    packages=find_packages(),
    classifiers=["Programming Language :: Python :: 3.7"],
    zip_safe=False,
)
