from pydantic import BaseModel, ConfigDict


class ProblemStateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    problemAlias: str
    status: str
    attempts: int
