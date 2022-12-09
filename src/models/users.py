from pydantic import BaseModel


class Users(BaseModel):
    uname: str
    pwhash: str
