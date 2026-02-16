from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import InvoiceCreateRequest, InvoiceResponse
from app.database import get_db
from app.db_models import Invoice
import uuid

router = APIRouter()

@router.post("/invoices", response_model=InvoiceResponse)
def create_invoice(data: InvoiceCreateRequest, db: Session = Depends(get_db)):
    invoice_id = f"inv-{uuid.uuid4().hex[:6]}"
    pdf_url = f"http://invoicing-service:8080/invoices/%7Binvoice_id%7D/pdf"  # URL for email API

    new_invoice = Invoice(
        invoiceId=invoice_id,
        orderId=data.orderId,
        userId=data.userId,
        amount=data.amount,
        status="created",
        pdfUrl=pdf_url
    )

    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)

    return new_invoice

@router.get("/invoices/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: str, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.invoiceId == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice