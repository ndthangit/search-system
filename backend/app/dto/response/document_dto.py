from pydantic import BaseModel, Field

class DocumentDto(BaseModel):
    link: str
    title_va: str = Field(alias="title-va")
    title_vska: str = Field(alias="title-vska")
    summary_va: str = Field(alias="summary-va")
    summary_vska: str = Field(alias="summary-vska")
    length: int
    last_updated: int

    class Config:
        allow_population_by_field_name = True
