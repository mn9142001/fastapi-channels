from pydantic import BaseModel
from typing import List, Union


class UserModel(BaseModel):
    id : int
    name: str
    img : str = "https://png.pngtree.com/png-clipart/20190520/original/pngtree-vector-users-icon-png-image_4144740.jpg"