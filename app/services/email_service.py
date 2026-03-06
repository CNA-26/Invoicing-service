import os
import requests


def send_invoice_email(email: str, name: str, invoice_id: str, amount: float, link: str):

    EMAIL_SERVICE_URL = os.getenv("EMAIL_SERVICE_URL")
    EMAIL_API_KEY = os.getenv("EMAIL_API_KEY")

    if not EMAIL_SERVICE_URL or not EMAIL_API_KEY:
        print("Email service env vars missing")
        return False, "Missing env variables"

    payload = {
        "email": email,
        "name": name,
        "invoiceId": invoice_id,
        "amount": amount,
        "link": link
    }

    headers = {
        "X-API-Key": EMAIL_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            f"{EMAIL_SERVICE_URL}/invoice",
            json=payload,
            headers=headers,
            timeout=10
        )

        print("Email status:", response.status_code)
        print("Email body:", response.text)

        return response.status_code == 200, response.text

    except Exception as e:
        print("Email request failed:", e)
        return False, str(e)