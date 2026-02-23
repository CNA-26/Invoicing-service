import os
import requests


def send_invoice_email(email: str, invoice_id: str, amount: float, pdf_url: str):

    EMAIL_SERVICE_URL = os.getenv("EMAIL_SERVICE_URL")
    EMAIL_API_KEY = os.getenv("EMAIL_API_KEY")

    if not EMAIL_SERVICE_URL or not EMAIL_API_KEY:
        print("Email service environment variables not set.")
        return None

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

        print("Email HTTP Status:", response.status_code)
        print("Email Response Text:", response.text)

        try:
            return response.json()
        except:
            return response.text

    except Exception as e:
        print("Error contacting email service:", e)
        return None