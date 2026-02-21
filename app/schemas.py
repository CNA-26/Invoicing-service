from pydantic import BaseModel

class InvoiceCreate(BaseModel):
    orderId: str

class InvoiceResponse(BaseModel):
    id: int
    order_id: str
    user_id: str
    amount: float
    status: str