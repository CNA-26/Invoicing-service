from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.models import InvoiceCreateRequest, InvoiceResponse
from app.order_data import orders
from app.pdf_generator import generate_invoice_pdf
from app.services.email_service import send_invoice_email
from app.database import get_db
from app.db_models import Invoice
from sqlalchemy.orm import Session
from fastapi import Depends
import uuid
import os

router = APIRouter()

PDF_FOLDER = os.getenv("PDF_FOLDER", "app/pdfs")
os.makedirs(PDF_FOLDER, exist_ok=True)

INVOICE_BASE_URL = "https://invoicing-service-git-cna-26.2.rahtiapp.fi"


@router.post("/invoices", response_model=InvoiceResponse)
def create_invoice(data: InvoiceCreateRequest, db: Session = Depends(get_db)):

    order = orders.get(data.orderId)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    invoice_id = f"inv-{uuid.uuid4().hex[:6]}"
    amount = sum(item["price"] for item in order["items"])

    invoice = Invoice(
        invoiceId=invoice_id,
        orderId=order["orderId"],
        userId=order["userId"],
        amount=amount,
        status="created",
        pdfUrl=f"{INVOICE_BASE_URL}/invoices/{invoice_id}/pdf"
    )

    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    pdf_bytes = generate_invoice_pdf(invoice.__dict__, order)

    pdf_path = f"{PDF_FOLDER}/{invoice_id}.pdf"

    with open(pdf_path, "wb") as f:
        f.write(pdf_bytes)

    send_invoice_email(
        email=order["email"],
        invoice_id=invoice_id,
        amount=amount,
        pdf_url=invoice.pdfUrl
    )

    return invoice


@router.get("/invoices/{invoice_id}/pdf")
def download_pdf(invoice_id: str):

    pdf_path = f"{PDF_FOLDER}/{invoice_id}.pdf"

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="Invoice PDF not found")

    return FileResponse(pdf_path, media_type="application/pdf")