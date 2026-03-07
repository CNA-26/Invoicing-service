from pydantic import BaseModel
from typing import Optional


class InvoiceCreateRequest(BaseModel):
    orderId: str
    email: Optional[str] = None