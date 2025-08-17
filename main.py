from fastapi import FastAPI, BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load .env variables
load_dotenv()

app = FastAPI()


origins = [
    "http://localhost:3000",  # your Next.js frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # allow GET, POST, OPTIONS etc.
    allow_headers=["*"],
)

# Email configuration
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("EMAIL_USER"),
    MAIL_PASSWORD=os.getenv("EMAIL_PASS"),
    MAIL_FROM=os.getenv("EMAIL_USER"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,   
    MAIL_SSL_TLS=False, 
    USE_CREDENTIALS=True
)

# Updated Order model to include productId and price
class Order(BaseModel):
    name: str
    email: EmailStr
    address: str
    product: str
    productId: str
    price: float
    quantity: int

@app.get("/")
async def root():
    return {"message": "CTC Backend is running! 🚀",
            "info": "working at the /send-order endpoint to send order emails."}


@app.post("/send-order")
async def send_order(order: Order, background_tasks: BackgroundTasks):
    # Email content
    body = f"""
📦 New Order Received:

Product: {order.product}
Product ID: {order.productId}
Quantity: {order.quantity}
Price per unit: ₹{order.price}

Shipping Address: {order.address}

Customer: {order.name}
Email: {order.email}
"""

    message = MessageSchema(
        subject=f"New Order: {order.product}",
        recipients=["jerryaryan123@email.com"],  # seller's email
        body=body,
        subtype="plain"
    )

    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)

    return {"message": "✅ Order email sent to seller!"}
