from pydantic import BaseModel


class InvoiceCreateRequest(BaseModel):
    orderId: str
    userId: str
    amount: float
    currency: str = "EUR"


class InvoiceResponse(BaseModel):
    invoiceId: str
    orderId: str
    userId: str
    amount: float
    status: str
    pdfUrl: str
