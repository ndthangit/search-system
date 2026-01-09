from pydantic import BaseModel, Field

class DocumentDto(BaseModel):
    link: str
    title_va: str = Field(alias="title-va")
    title_vska: str = Field(alias="title-vska")
    content_va: str = Field(alias="content-va")
    content_vska: str = Field(alias="content-vska")
    length: int
    last_updated: str

    class Config:
        allow_population_by_field_name = True
