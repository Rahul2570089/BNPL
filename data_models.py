from datetime import datetime
from enum import Enum

class PaymentMode(Enum):
    PREPAID = "PREPAID"
    BNPL = "BNPL"

class OrderStatus(Enum):
    PLACED = "PLACED"
    PAID = "PAID"
    DEFAULTED = "DEFAULTED"

class Product:
    def __init__(self, product_id, name, category, price=100, description=""):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.description = description

    def __str__(self):
        return f"Product(id={self.product_id}, name={self.name}, category={self.category}, price={self.price}, description={self.description})"
    
class InventoryItem:
    def __init__(self, product: Product, quantity):
        self.product = product
        self.quantity = quantity
    
    def __str__(self):
        return f"InventoryItem(product={self.product}, quantity={self.quantity})"

class Order:
    def __init__(self, order_id, product_id, user_id, quantity, payment_mode, order_date, due_date, status, amount_paid, remaining_amount):
        self.order_id = order_id
        self.product_id = product_id
        self.user_id = user_id
        self.quantity = quantity
        self.payment_mode = payment_mode
        self.order_date = order_date
        self.due_date = due_date
        self.status = status
        self.amount_paid = amount_paid
        self.remaining_amount = remaining_amount
    
    def is_defaulted(self) -> bool:
        return self.payment_mode == PaymentMode.BNPL and self.remaining_amount > 0 and datetime.now() > self.due_date

    
    def __str__(self):
        return (f"Order(id={self.order_id}, product_id={self.product_id}, user_id={self.user_id}, quantity={self.quantity}, "
                f"payment_mode={self.payment_mode}, order_date={self.order_date}, due_date={self.due_date}, status={self.status}, "
                f"amount_paid={self.amount_paid}, remaining_amount={self.remaining_amount})")
    
class User:
    def __init__(self, user_id, name, credit_limit):
        self.user_id = user_id
        self.name = name
        self.credit_limit = credit_limit
        self.used_credit = 0.0
        self.is_blacklisted = False
        self.default_count = 0

    def available_credit(self) -> float:
        return self.credit_limit - self.used_credit

    def __str__(self):
        return (f"User(id={self.user_id}, name={self.name}, credit_limit={self.credit_limit}, "
                f"used_credit={self.used_credit}, is_blacklisted={self.is_blacklisted}, default_count={self.default_count})")
