from sqlalchemy import Column, String, Float
from app.database import Base
import uuid

class Invoice(Base):
    __tablename__ = "invoices"

    invoiceId = Column(String, primary_key=True, default=lambda: f"inv-{uuid.uuid4().hex[:6]}")
    orderId = Column(String, nullable=False)
    userId = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, default="created")
    pdfUrl = Column(String, nullable=False)