from pydantic import BaseModel


class Progress(BaseModel):
    frame: int
    fps: float
    size: int
    time: str
    bitrate: float
    speed: float
