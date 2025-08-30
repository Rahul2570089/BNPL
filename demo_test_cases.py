from datetime import timedelta
from bnpl import *

def run_comprehensive_demo():
    print("Starting BNPL System Demo")
    print("=" * 50)
    
    system = BNPLSystem()
    
    print("\nADDING PRODUCTS TO INVENTORY")
    print("-" * 30)
    
    products = [
        Product("P001", "iPhone 15", "Electronics", 50999.99, "Apple smartphone"),
        Product("P002", "MacBook Air", "Electronics", 129999.99, "Apple laptop"),
        Product("P003", "Nike Shoes", "Fashion", 4299.99, "Running shoes"),
        Product("P004", "Puma Shoes", "Fashion", 2299.99, "Running shoes"),
    ]
    
    for product in products:
        system.add_product_to_inventory(product, 10)
    
    print("\nADDING USERS")
    print("-" * 15)
    
    users = [
        User("U001", "Rahul", 52000.0),
        User("U002", "Rohit", 2000.0),
        User("U003", "Aman", 1000.0),
    ]
    
    for user in users:
        system.add_user(user)
    
    print("\nTESTING ORDER SCENARIOS")
    print("-" * 25)
    
    print("\n1. Testing successful prepaid order:")
    system.place_order("U001", "P003", 2, PaymentMode.PREPAID)
    
    print("\n2. Testing successful BNPL order:")
    system.place_order("U001", "P001", 1, PaymentMode.BNPL)
    
    print("\n3. Testing BNPL order exceeding credit limit:")
    system.place_order("U002", "P002", 2, PaymentMode.BNPL)
    
    print("\n4. Testing order with insufficient inventory:")
    system.place_order("U001", "P001", 15, PaymentMode.PREPAID)
    
    print("\n5. Testing multiple BNPL orders:")
    system.place_order("U002", "P003", 5, PaymentMode.BNPL)
    system.place_order("U002", "P004", 3, PaymentMode.BNPL)
    
    print("\nTESTING PAYMENT CLEARING")
    print("-" * 25)
    
    print("\n1. Partial payment:")
    system.clear_dues("U001", 500.0)
    
    print("\n2. Full payment:")
    system.clear_dues("U001", 600.0)
    
    print("\nTESTING STATUS QUERIES")
    print("-" * 23)
    
    print("\n1. Inventory Status:")
    inventory = system.get_inventory_status()
    for pid, details in inventory.items():
        print(f"   {pid}: {details["name"]} - Qty: {details["quantity"]}, Price: ₹{details["price"]}")
    
    print("\n2. User Status:")
    for user_id in ["U001", "U002", "U003"]:
        status = system.get_user_status(user_id)
        if "error" not in status:
            print(f"   {user_id}: Credit: ₹{status["available_credit"]}/₹{status["credit_limit"]}, "
                  f"Dues: ₹{status["total_pending_dues"]}, Orders: {status["total_orders"]}")
    
    print("\n3. Order History for U002:")
    history = system.get_user_order_history("U002")
    for order in history:
        if "error" not in order:
            print(f"   Order {order["order_id"][:8]}: {order["product_name"]} x{order["quantity"]} - "
                  f"₹{order["total_amount"]} ({order["payment_mode"]}) - {order["status"]}")
    
    print("\nTESTING BLACKLISTING SCENARIO")
    print("-" * 30)
    
    print("\n1. Creating user prone to defaults:")
    test_user = User("U999", "Test User", 500.0)
    system.add_user(test_user)
    
    print("\n2. Simulating default scenario:")
    
    order1 = system.place_order("U999", "P004", 2, PaymentMode.BNPL)
    order2 = system.place_order("U999", "P003", 1, PaymentMode.BNPL)
    order3 = system.place_order("U999", "P004", 1, PaymentMode.BNPL)
    
    if order1:
        system.orders[order1].due_date = datetime.now() - timedelta(days=5)
    if order2:
        system.orders[order2].due_date = datetime.now() - timedelta(days=3)
    if order3:
        system.orders[order3].due_date = datetime.now() - timedelta(days=1)
    
    print("\n3. Checking for defaults and blacklisting:")
    system.check_and_update_defaults("U999")
    
    print("\n4. Trying to place new BNPL order with blacklisted user:")
    system.place_order("U999", "P004", 1, PaymentMode.BNPL)
    
    print("\n5. Blacklisted user can still place prepaid orders:")
    system.place_order("U999", "P004", 1, PaymentMode.PREPAID)
    
    print("\nDemo completed successfully!")
    print("=" * 50)

def run_edge_case_tests():
    print("\nRUNNING EDGE CASE TESTS")
    print("=" * 30)
    
    system = BNPLSystem()
    
    print("\n1. Testing invalid user operations:")
    result = system.place_order("INVALID_USER", "P001", 1, PaymentMode.PREPAID)
    assert result is None, "Should return None for invalid user"
    
    print("2. Testing invalid product operations:")
    system.add_user(User("TEST", "Test User", credit_limit=5000.0))
    result = system.place_order("TEST", "INVALID_PRODUCT", 1, PaymentMode.PREPAID)
    assert result is None, "Should return None for invalid product"
    
    print("3. Testing zero/negative quantities:")
    system.add_product_to_inventory(Product("TEST_P", "Test Product", 10.0), 5)
    result = system.place_order("TEST", "TEST_P", 0, PaymentMode.PREPAID)
    
    print("4. Testing negative payment amount:")
    result = system.clear_dues("TEST", -100.0)
    assert result is False, "Should return False for negative payment"
    
    print("5. Testing floating point precision:")
    system.clear_dues("TEST", 0.01)
    
    print("Edge case tests completed!")

if __name__ == "__main__":
    run_comprehensive_demo()
    
    run_edge_case_tests()