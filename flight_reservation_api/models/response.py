from pydantic import BaseModel
from typing import Optional


class Status(BaseModel):
    status: Optional[str]
    reason: Optional[str]
