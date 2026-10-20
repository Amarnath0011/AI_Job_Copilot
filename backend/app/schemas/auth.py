from pydantic import BaseModel , EmailStr , Field

class SignupRequest(BaseModel):
    name:str = Field(min_len = 2 , max_len = 50),
    email: EmailStr
    password : str = Field(min_len = 8 , max_len = 100)