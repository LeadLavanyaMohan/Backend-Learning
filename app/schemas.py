from pydantic import BaseModel

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True #defalt value

class PostCreate(PostBase):
    pass


 