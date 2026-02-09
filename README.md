# Invoicing Service API

---

What we have for now:

- A working live API endpoint
- Hardcoded placeholder invoice data (no database yet)
- REST client testing file

---

## Base URL (Rahti Deployment)

```bash
https://invoicing-service-git-cna-26.2.rahtiapp.fi/
```

---

## Running Locally

### 1. Install requirements

```bash
pip install -r requirements.txt
```

2. Start the server

```bash
uvicorn app.main:app --reload --port 8080
```
The API will be available at:
```bash
http://localhost:8080
```

Swagger documentation:

```bash
http://localhost:8080/docs
```

### Running with Docker

Build and run locally

```bash
docker-compose up --build
```

The service will run on:

```bash
http://localhost:8080
```

### Health Check Endpoint

Used to verify that the service is running.

Example:

```bash
GET /health
```

Response:
```bash
{
  "status": "ok"
}
```

## API Endpoints

### Create Invoice

```bash
POST /invoices
```

Creates an invoice from an order.

Request body:
```bash
{
  "orderId": "order-123",
  "userId": "user-42",
  "amount": 49.90,
  "currency": "EUR"
}
```
Response:
```bash
{
  "invoiceId": "inv-abc123",
  "orderId": "order-123",
  "userId": "user-42",
  "amount": 49.90,
  "status": "created",
  "pdfUrl": "placeholder.pdf"
}
```
### Get Invoice by ID
```bash
GET /invoices/{invoiceId}
```
Fetches invoice details.

Example:
```bash
GET /invoices/inv-001
```
Response:
```bash
{
  "invoiceId": "inv-001",
  "orderId": "order-123",
  "userId": "user-42",
  "amount": 49.90,
  "status": "created",
  "pdfUrl": "placeholder.pdf"
}
```

### Endpoint Testing

A REST client test file is included:

```bash
invoicing.rest
```
Example test:

```bash
### Health check
GET https://invoicing-service-git-cna-26.2.rahtiapp.fi/health

### Create invoice
POST https://invoicing-service-git-cna-26.2.rahtiapp.fi/invoices
Content-Type: application/json

{
  "orderId": "order-123",
  "userId": "user-42",
  "amount": 49.90
}
```