from pydantic import BaseModel , Field
from datetime import datetime
from typing import Optional

class UrlBase(BaseModel):
    url: str = Field (..., description="The url is required",)
    status: str = Field("up", description="the status of the url", example="up") 

class UrlCreate(UrlBase):
    pass  

class UrlSchema(UrlBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  