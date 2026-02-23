from pydantic import BaseModel

class InvoiceCreate(BaseModel):
    orderId: str
    userId: str
    email: str
    amount: float
    currency: str


class InvoiceResponse(BaseModel):
    invoiceId: str
    orderId: str
    userId: str
    email: str
    amount: float
    currency: str
    status: str
    pdfUrl: str

    class Config:
        orm_mode = True