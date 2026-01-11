from pydantic import BaseModel, Field

class DocumentDto(BaseModel):
    link: str
    title_va: str = Field(alias="title-va")
    content_va: str = Field(alias="content-va")
    length: int
    last_updated: str

    class Config:
        allow_population_by_field_name = True
