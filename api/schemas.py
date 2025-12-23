from pydantic import BaseModel


class DrowsinessStatus(BaseModel):
    ear: float
    drowsy: bool
    attention: str
