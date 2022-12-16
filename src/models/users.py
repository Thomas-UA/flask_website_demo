from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class UserModel(BaseModel):
    uname: str
    pwhash: str
    favorite: Optional[str] = "not specified"
    registration_date = datetime.now()


class UserFront(BaseModel):
    uname: str
    favorite: str
