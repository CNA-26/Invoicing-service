from sqlalchemy import Column, String, Float
from app.database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    invoiceId = Column(String, primary_key=True, index=True)
    orderId = Column(String)
    userId = Column(String)
    email = Column(String)
    amount = Column(Float)
    currency = Column(String)
    status = Column(String)
    pdfUrl = Column(String)