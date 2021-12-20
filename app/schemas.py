from typing import Optional
from pydantic import BaseModel, EmailStr

from app.database import Base

#Creating our data model
class Post(BaseModel): #A pydantic model (to validate the data in request method which is fed to our api)
    title : str
    content : str
    published : bool
    # published : bool = True #sets the default value of published as True, now if we dont give value of 'published', it wont throw an error
    # rating: Optional[int] = None #states that rating is not a compulsory input, and by default it will have a None value. also it will throw error if we enter a non integer entry.
# any input that inherits from this model must have these fields, and the corresponding datatype.

#pydantic model is just a validation step, to keep a check on the user input. This is not the actual table where data is stored.
#the actual database table is the sqlalchemy model created in the models.py folder

class UserOut(BaseModel):
    email : EmailStr
    id : int

    class Config: #This helps to avoid 'value is not a valid dict' error, by converting sqlalchemy model object to a python dictionary
        orm_mode = True

# a pydantic model to validate the response from our api to the user.
class Post_new(Post): #This model is inherited from Post model which was created above.
# ie : it has all the attributes of parent model (title, content, published), on top of that it has additional attributes (id in this case)
    id : int
    owner_id: int
    owner : UserOut #validates the output from relation method from models.py as one of the prebuilt pydantic schemas "UserOut"

    class Config: #This helps to avoid 'value is not a valid dict' error, by converting sqlalchemy model object to a python dictionary
        orm_mode = True

class UserCreate(BaseModel):
    email : EmailStr
    password : str



class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id: Optional[str]=None