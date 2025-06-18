from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str


class UserSchema(BaseModel):
    # TODO: Probably need to handle exposing the ID in the response later
    id: int | None = None
    name: str
    customer_id: str | None = None

    class Config:
        from_attributes = True
