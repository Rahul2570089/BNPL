from typing import Dict, List, Optional
from data_models import *
import uuid

class BNPLSystem:
    def __init__(self):
        self.inventory: Dict[str, InventoryItem] = {}
        self.users: Dict[str, User] = {}
        self.orders: Dict[str, Order] = {}
        self.user_orders: Dict[str, List[str]] = {}

    def add_product_to_inventory(self, product: Product, quantity: int) -> bool:
        try:
            if product.product_id in self.inventory:
                self.inventory[product.product_id] += quantity
            else:
                self.inventory[product.product_id] = InventoryItem(product, quantity)
            print(f"Added {quantity} units of product {product.name} to inventory")
            return True
        except Exception as e:
            print(f"Error adding product to inventory: {e}")
            return False
    
    def get_inventory_status(self, product_id: Optional[str] = None) -> Dict:
        try:
            if product_id:
                if product_id in self.inventory:
                    item = self.inventory[product_id]
                    return {
                        "product_id": product_id,
                        "name": item.product.name,
                        "price": item.product.price,
                        "quantity": item.quantity,
                        "category": item.product.category
                    }
                else:
                    return {"error": f"Product {product_id} not found in inventory"}
            # if no product_id is provided then return all product status
            else:
                result = {}
                for pid, item in self.inventory.items():
                    result[pid] = {
                        "product_id": product_id,
                        "name": item.product.name,
                        "price": item.product.price,
                        "quantity": item.quantity,
                        "category": item.product.category
                    }
                return result
        except Exception as e:
            return {"error": f"Error checking inventory status: {e}"}
    
    def add_user(self, user: User):
        try:
            self.users[user.user_id] = user
            self.user_orders[user.user_id] = []
            print(f"Added user {user.name} successfully")
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
    
    def check_and_update_defaults(self, user_id: str):
        if user_id not in self.user_orders:
            print(f"User with id {user_id} has no orders yet")
            return
        
        current_defaults = 0
        for order_id in self.user_orders[user_id]:
            order = self.orders[order_id]
            if order.is_defaulted() and order.status != OrderStatus.DEFAULTED:
                order.status = OrderStatus.DEFAULTED
                current_defaults += 1
                print(f"Order {order_id} has been marked as defaulted")
        
        if current_defaults > 0:
            self.users[user_id].default_count += current_defaults
            if self.users[user_id].default_count >= 3:
                self.users[user_id].is_blacklisted = True
                print(f"User {user_id} has been blacklisted due to >=3 defaults")
    
    def place_order(self, user_id: str, product_id: str, quantity: int, payment_mode: PaymentMode) -> Optional[str]:
        try:
            if user_id not in self.users:
                print(f"User {user_id} not found")
                return None
            
            user = self.users[user_id]
            
            self.check_and_update_defaults(user_id)
            
            if product_id not in self.inventory:
                print(f"Product {product_id} not found in inventory")
                return None
            
            inventory_item = self.inventory[product_id]
            if inventory_item.quantity < quantity:
                print(f"Insufficient inventory. Available: {inventory_item.quantity}, Requested: {quantity}")
                return None
            
            total_amount = inventory_item.product.price * quantity
            
            if payment_mode == PaymentMode.BNPL:
                if user.is_blacklisted:
                    print(f"User {user_id} is blacklisted and cannot use BNPL")
                    return None
                
                if user.available_credit() < total_amount:
                    print(f"Insufficient credit. Available: ${user.available_credit()}, Required: ${total_amount}")
                    return None
            
            order_id = str(uuid.uuid4())
            order = Order(order_id, user_id, product_id, quantity, total_amount, payment_mode)
            
            inventory_item.quantity -= quantity
            
            if payment_mode == PaymentMode.BNPL:
                user.used_credit += total_amount
            
            self.orders[order_id] = order
            self.user_orders[user_id].append(order_id)
            
            print(f"Order placed successfully: {order_id}")
            print(f"Order details: {order}")
            return order_id
            
        except Exception as e:
            print(f" Error placing order: {e}")
            return None
    
    def clear_dues(self, user_id: str, amount: float) -> bool:
        try:
            if user_id not in self.users:
                print(f"User {user_id} not found")
                return False
            
            if amount <= 0:
                print(f"Payment amount must be positive")
                return False
            
            user = self.users[user_id]
            remaining_payment = amount
            
            bnpl_orders = []
            for order_id in self.user_orders[user_id]:
                order = self.orders[order_id]
                if order.payment_mode == PaymentMode.BNPL and order.remaining_amount > 0:
                    bnpl_orders.append(order)
            
            if not bnpl_orders:
                print(f"No pending dues for user {user_id}")
                return True
            
            bnpl_orders.sort(key=lambda x: x.due_date)
            
            for order in bnpl_orders:
                if remaining_payment <= 0:
                    break
                
                payment_for_this_order = min(remaining_payment, order.remaining_amount)
                order.amount_paid += payment_for_this_order
                order.remaining_amount -= payment_for_this_order
                remaining_payment -= payment_for_this_order
                
                if order.remaining_amount <= 0.01:
                    order.remaining_amount = 0.0
                    order.status = OrderStatus.PAID
                    print(f"Order {order.order_id} fully paid")
                else:
                    print(f"Partial payment of ${payment_for_this_order} applied to order {order.order_id}")
            
            credit_freed = amount - remaining_payment
            user.used_credit -= credit_freed
            
            print(f"Payment of ${credit_freed} processed for user {user_id}")
            if remaining_payment > 0:
                print(f"${remaining_payment} could not be applied (no pending dues)")
            
            return True
            
        except Exception as e:
            print(f"Error processing payment: {e}")
            return False
    
    def get_user_order_history(self, user_id: str) -> List[Dict]:
        try:
            if user_id not in self.users:
                return [{"error": f"User {user_id} not found"}]
            
            self.check_and_update_defaults(user_id)
            
            history = []
            for order_id in self.user_orders[user_id]:
                order = self.orders[order_id]
                product = self.inventory[order.product_id].product
                
                history.append({
                    "order_id": order.order_id,
                    "product_name": product.name,
                    "quantity": order.quantity,
                    "total_amount": order.total_amount,
                    "payment_mode": order.payment_mode.value,
                    "status": order.status.value,
                    "order_date": order.order_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "due_date": order.due_date.strftime("%Y-%m-%d %H:%M:%S") if order.due_date else None,
                    "amount_paid": order.amount_paid,
                    "remaining_amount": order.remaining_amount,
                    "is_defaulted": order.is_defaulted()
                })
            
            return history
            
        except Exception as e:
            return [{"error": f"Error retrieving order history: {e}"}]
    
    def get_user_status(self, user_id: str) -> Dict:
        try:
            if user_id not in self.users:
                return {"error": f"User {user_id} not found"}
            
            self.check_and_update_defaults(user_id)
            
            user = self.users[user_id]
            
            total_dues = sum(order.remaining_amount for order_id in self.user_orders[user_id] 
                           for order in [self.orders[order_id]] 
                           if order.payment_mode == PaymentMode.BNPL and order.remaining_amount > 0)
            
            order_counts = {"PLACED": 0, "PAID": 0, "DEFAULTED": 0}
            for order_id in self.user_orders[user_id]:
                order = self.orders[order_id]
                order_counts[order.status.value] += 1
            
            return {
                "user_id": user.user_id,
                "name": user.name,
                "credit_limit": user.credit_limit,
                "used_credit": user.used_credit,
                "available_credit": user.available_credit(),
                "is_blacklisted": user.is_blacklisted,
                "default_count": user.default_count,
                "total_pending_dues": total_dues,
                "total_orders": len(self.user_orders[user_id]),
                "order_counts": order_counts
            }
            
        except Exception as e:
            return {"error": f"Error retrieving user status: {e}"}

