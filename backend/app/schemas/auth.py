from pydantic import AliasChoices, BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    full_name: str = Field(
        min_length=2,
        max_length=100,
        validation_alias=AliasChoices("full_name", "name"),
    )
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=72)


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
