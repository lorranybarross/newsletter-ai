from pydantic import BaseModel, Field

class SearchResult(BaseModel):
    title: str = Field(description='Title of selected news')
    snippet: str = Field(description='A snippet of selected news')
    url: str = Field(description='The URL of selected news')
