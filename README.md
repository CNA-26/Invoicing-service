# Invoicing Service API

A FastAPI microservice that creates invoices, generates a PDF, stores invoice data in PostgreSQL and sends the invoice to the Email Service.

Currently the Order Service is not integrated yet, so placeholder order data is used.

---

# Features

- FastAPI REST API
- PostgreSQL database (SQLAlchemy)
- Invoice stored in database
- PDF invoice generation
- PDF download endpoint
- Integration with Email Service
- Basic error handling
- Docker support

---

# Base URL (Rahti Deployment)

```
https://invoicing-service-git-cna-26.2.rahtiapp.fi/
```

---

# API Endpoints

## Health Check

Used to verify that the service is running.

```
GET /health
```

Response

```json
{
  "status": "ok"
}
```

---

# Create Invoice

Creates an invoice from an order.

```
POST /invoices
```

Request

```json
{
  "orderId": "order-123"
}
```

Example response

```json
{
  "invoiceId": "inv-abc123",
  "orderId": "order-123",
  "userId": "user-42",
  "email": "customer@example.com",
  "amount": 49.9,
  "currency": "EUR",
  "status": "email_sent",
  "pdfUrl": "http://localhost:8080/invoices/inv-abc123/pdf"
}
```

---

# Download Invoice PDF

```
GET /invoices/{invoiceId}/pdf
```

Returns the generated PDF invoice.

Example

```
GET /invoices/inv-abc123/pdf
```

---

# Running Locally

Install dependencies

```bash
pip install -r requirements.txt
```

Start the API

```bash
uvicorn app.main:app --reload --port 8080
```

API available at

```
http://localhost:8080
```

Swagger documentation

```
http://localhost:8080/docs
```

---

# Running with Docker

Start containers

```bash
docker-compose up --build
```

Service runs at

```
http://localhost:8080
```

---

# Database

The service uses PostgreSQL and stores invoices in the `invoices` table.

Stored fields:

- invoiceId
- orderId
- userId
- email
- amount
- currency
- status
- pdfUrl

---

# Notes

- Order Service is not integrated yet
- Placeholder order data is used for testing
- Email sending is handled via Email Service API