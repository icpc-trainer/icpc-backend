from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TrainingSessionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: str
    dt_created: datetime
