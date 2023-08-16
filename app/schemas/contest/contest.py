from pydantic import BaseModel, ConfigDict, Field


class ContestSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
