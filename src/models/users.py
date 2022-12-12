from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class UserModel(BaseModel):
    uname: str
    pwhash: bytes
    favorite: Optional[str] = "not specified"
    registration_date = datetime.now()
