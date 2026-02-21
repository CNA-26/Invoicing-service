import requests
import os

EMAIL_SERVICE_URL = os.getenv("EMAIL_SERVICE_URL")
EMAIL_API_KEY = os.getenv("EMAIL_API_KEY")


def send_invoice_email(email, invoice_id, amount, pdf_url):
    if not EMAIL_SERVICE_URL:
        print("Email service URL not configured")
        return

    try:
        response = requests.post(
            f"{EMAIL_SERVICE_URL}/invoice",
            headers={
                "x-api-key": EMAIL_API_KEY,
                "Authorization": "Bearer dummy"
            },
            json={
                "email": email,
                "invoiceId": invoice_id,
                "amount": amount,
                "pdfUrl": pdf_url
            }
        )

        print("Email service response:", response.text)

    except Exception as e:
        print("Email service failed:", e)