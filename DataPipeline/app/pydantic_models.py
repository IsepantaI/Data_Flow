from typing import List,Optional
from datetime import datetime
from pydantic import BaseModel


class FundItems(BaseModel):
    regNo: str
    name: str
    fundType: int
    netAsset: Optional[int] = None



class FundAPIResponse(BaseModel):
    status: int
    message: str
    pageNumber: int
    pageSize: int
    totalCount: int
    items: List[FundItems]


