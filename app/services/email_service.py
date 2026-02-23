import os
import requests


def send_invoice_email(email: str, invoice_id: str, amount: float, pdf_url: str):
    """
    Sends invoice data to the Email Service.
    Does NOT raise exceptions to avoid breaking invoice creation.
    """

    EMAIL_SERVICE_URL = os.getenv("EMAIL_SERVICE_URL")
    EMAIL_API_KEY = os.getenv("EMAIL_API_KEY")

    if not EMAIL_SERVICE_URL or not EMAIL_API_KEY:
        print("Email service environment variables not set.")
        return False

    try:
        response = requests.post(
            f"{EMAIL_SERVICE_URL}/invoice",
            json={
                "email": email,
                "invoiceId": invoice_id,
                "amount": amount
            },
            headers={
                "X-API-Key": EMAIL_API_KEY,
                "Content-Type": "application/json"
            },
            timeout=5
        )

        if response.status_code == 200:
            print("Email sent successfully")
            return True
        else:
            print(f"Email failed: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"Error contacting email service: {e}")
        return False