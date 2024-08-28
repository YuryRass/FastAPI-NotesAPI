from pydantic import BaseModel, EmailStr


class SUserAuth(BaseModel):
    email: EmailStr
    password: str


class SUserOut(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True
