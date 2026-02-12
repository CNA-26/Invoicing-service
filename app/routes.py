from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.models import InvoiceCreateRequest, InvoiceResponse
from app.order_data import orders
from app.pdf_generator import generate_invoice_pdf

import uuid
import os
import requests

router = APIRouter()

PDF_FOLDER = "app/pdfs"
os.makedirs(PDF_FOLDER, exist_ok=True)

EMAIL_SERVICE_URL = "http://email-service:3000/invoice"
INVOICE_BASE_URL = "http://localhost:8080"

@router.post("/invoices", response_model=InvoiceResponse)
def create_invoice(data: InvoiceCreateRequest):

    order = orders.get(data.orderId)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    invoice_id = f"inv-{uuid.uuid4().hex[:6]}"

    amount = sum(item["price"] for item in order["items"])

    invoice = {
        "invoiceId": invoice_id,
        "orderId": order["orderId"],
        "userId": order["userId"],
        "amount": amount,
        "status": "created",
        "pdfUrl": f"{INVOICE_BASE_URL}/invoices/{invoice_id}/pdf"
    }

    pdf_bytes = generate_invoice_pdf(invoice, order)

    pdf_path = f"{PDF_FOLDER}/{invoice_id}.pdf"

    with open(pdf_path, "wb") as f:
        f.write(pdf_bytes)

    try:
        requests.post(
            EMAIL_SERVICE_URL,
            headers={
                "Authorization": "Bearer YOUR_JWT_TOKEN"
            },
            json={
                "email": order["email"],
                "invoiceId": invoice_id,
                "amount": amount,
                "pdfUrl": invoice["pdfUrl"]
            }
        )
    except Exception as e:
        print("Email service call failed:", e)

    return invoice

@router.get("/invoices/{invoice_id}/pdf")
def download_invoice_pdf(invoice_id: str):

    pdf_path = f"{PDF_FOLDER}/{invoice_id}.pdf"

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="Invoice PDF not found")

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"{invoice_id}.pdf"
    )
