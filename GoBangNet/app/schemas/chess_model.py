from pydantic import BaseModel
from typing import List


class chess_model(BaseModel):
    chess: List[int]

