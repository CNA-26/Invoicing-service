import os
import requests


def send_invoice_email(email: str, name: str, invoice_id: str, amount: float, link: str):
    EMAIL_SERVICE_URL = os.getenv("EMAIL_SERVICE_URL")
    EMAIL_API_KEY = os.getenv("EMAIL_API_KEY")

    print("========== EMAIL SERVICE DEBUG ==========")
    print("EMAIL_SERVICE_URL:", EMAIL_SERVICE_URL)
    print("EMAIL_API_KEY exists:", bool(EMAIL_API_KEY))

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

    url = EMAIL_SERVICE_URL.rstrip("/") + "/invoice"

    print("FINAL EMAIL REQUEST")
    print("URL:", url)
    print("HEADERS:", headers)
    print("PAYLOAD:", payload)

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=10
        )

        print("Email Status:", response.status_code)
        print("Email Response:", response.text)
        print("=========================================")

        return response.status_code == 200, response.text

    except Exception as e:
        print("mail Request Failed:", e)
        return False, str(e)