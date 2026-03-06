from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.models import InvoiceCreateRequest
from app.schemas import InvoiceResponse
from app.order_data import orders
from app.pdf_generator import generate_invoice_pdf
from app.services.email_service import send_invoice_email
from app.database import get_db
from app.db_models import Invoice
import uuid
import os

router = APIRouter()

PDF_FOLDER = os.getenv("PDF_FOLDER", "app/pdfs")
os.makedirs(PDF_FOLDER, exist_ok=True)

INVOICE_BASE_URL = os.getenv(
    "INVOICE_BASE_URL",
    "http://localhost:8080"
)


@router.post("/invoices", response_model=InvoiceResponse)
def create_invoice(data: InvoiceCreateRequest, db: Session = Depends(get_db)):

    order = orders.get(data.orderId)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    print("ORDER FROM ORDER SERVICE:", order)

    invoice_id = f"inv-{uuid.uuid4().hex[:6]}"
    amount = sum(item["price"] for item in order["items"])
    pdf_url = f"{INVOICE_BASE_URL}/invoices/{invoice_id}/pdf"

    invoice = Invoice(
        invoiceId=invoice_id,
        orderId=order["orderId"],
        userId=order["userId"],
        email=order["email"],
        amount=amount,
        currency="EUR",
        status="created",
        pdfUrl=pdf_url
    )

    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    pdf_bytes = generate_invoice_pdf(invoice.__dict__, order)

    pdf_path = os.path.join(PDF_FOLDER, f"{invoice_id}.pdf")
    with open(pdf_path, "wb") as f:
        f.write(pdf_bytes)

    payload = {
        "email": order["email"],
        "name": "Customer",
        "invoiceId": invoice_id,
        "amount": amount,
        "link": pdf_url
    }

    print("EMAIL PAYLOAD FINAL:", payload)

    email_success, email_response = send_invoice_email(
        email=payload["email"],
        name=payload["name"],
        invoice_id=payload["invoiceId"],
        amount=payload["amount"],
        link=payload["link"]
    )

    print("EMAIL SUCCESS:", email_success)
    print("EMAIL RESPONSE:", email_response)

    invoice.status = "email_sent" if email_success else "email_failed"

    db.commit()
    db.refresh(invoice)

    return invoice


@router.get("/invoices/{invoice_id}/pdf")
def download_pdf(invoice_id: str):

    pdf_path = os.path.join(PDF_FOLDER, f"{invoice_id}.pdf")

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="Invoice PDF not found")

    return FileResponse(pdf_path, media_type="application/pdf")