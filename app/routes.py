from fastapi import APIRouter, HTTPException
from app.models import InvoiceCreateRequest, InvoiceResponse
from app.placeholder_data import invoices
import uuid

router = APIRouter()


@router.post("/invoices", response_model=InvoiceResponse)
def create_invoice(data: InvoiceCreateRequest):

    new_invoice = {
        "invoiceId": f"inv-{uuid.uuid4().hex[:6]}",
        "orderId": data.orderId,
        "userId": data.userId,
        "amount": data.amount,
        "status": "created",
        "pdfUrl": "placeholder.pdf"
    }

    invoices.append(new_invoice)
    return new_invoice


@router.get("/invoices/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: str):

    for inv in invoices:
        if inv["invoiceId"] == invoice_id:
            return inv

    raise HTTPException(status_code=404, detail="Invoice not found")
