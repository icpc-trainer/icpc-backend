from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TrainingSessionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: str
