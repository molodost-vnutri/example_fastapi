from pydantic import BaseModel, Field

class STasks(BaseModel):
    name: str = Field(min_length=4, max_length=35)
    title: str
    public: bool = True