from pydantic import BaseModel


class InvoiceCreateRequest(BaseModel):
    orderId: str
