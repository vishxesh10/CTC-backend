from fastapi import FastAPI, BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

app = FastAPI()

# Email configuration (using Gmail SMTP as example)
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("EMAIL_USER"),
    MAIL_PASSWORD=os.getenv("EMAIL_PASS"),
    MAIL_FROM=os.getenv("EMAIL_USER"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)

# Data model for incoming request
class Order(BaseModel):
    name: str
    email: EmailStr
    address: str
    product: str
    quantity: int

@app.post("/send-order")
async def send_order(order: Order, background_tasks: BackgroundTasks):
    # Email content/ template
    body = f"""
    📦 New Order Received:

    Product: {order.product}
    Quantity: {order.quantity}
    
    Address: {order.address}

    Customer: {order.name}
    Email: {order.email}
    """

    message = MessageSchema(
        subject=f"New Order: {order.product}",
        recipients=["jerryaryan123@email.com"], #sellers mail
        body=body,
        subtype="plain"
    )

    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)

    return {"message": "✅ Order email sent to seller!"}
