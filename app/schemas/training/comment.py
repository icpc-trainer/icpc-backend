from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CommentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    userId: int
    userFirstName: str
    userLastName: str
    userLogin: str
    problemAlias: str
    content: str


