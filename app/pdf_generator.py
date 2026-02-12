from reportlab.pdfgen import canvas
import io


def generate_invoice_pdf(invoice, order):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)

    c.setFont("Helvetica-Bold", 18)
    c.drawString(200, 800, "INVOICE")

    c.setFont("Helvetica", 12)
    c.drawString(50, 760, f"Invoice ID: {invoice['invoiceId']}")
    c.drawString(50, 740, f"Order ID: {invoice['orderId']}")
    c.drawString(50, 720, f"User ID: {invoice['userId']}")
    c.drawString(50, 700, f"Amount: {invoice['amount']} EUR")

    c.drawString(50, 660, "Items:")

    y = 640
    for item in order["items"]:
        c.drawString(70, y, f"- {item['name']} ({item['price']} EUR)")
        y -= 20

    c.drawString(50, y - 20, "Thank you for your purchase!")

    c.save()

    buffer.seek(0)
    return buffer.read()
