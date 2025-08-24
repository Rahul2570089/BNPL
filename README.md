## Testing

Run the comprehensive demo to see all features in action:

```bash
python demo_test_cases.py
```

The demo includes:
- Product and user setup
- Various order scenarios
- Payment processing
- Status reporting
- Blacklisting simulation
- Edge case testing

# BNPL (Buy Now, Pay Later) System

A comprehensive Buy Now, Pay Later system implementation in Python that manages inventory, users, orders, and credit facilities with automatic default detection and blacklisting functionality.

## Features

### Core Functionality
- **Inventory Management**: Add products and track stock levels
- **User Management**: Register users with credit limits and track payment history
- **Order Processing**: Support both prepaid and BNPL payment modes
- **Credit Management**: Track used credit, available credit, and enforce limits
- **Payment Processing**: Clear dues with automatic payment allocation
- **Default Detection**: Automatically detect overdue payments and mark as defaulted
- **Blacklisting**: Automatically blacklist users with 3+ defaults

### Key Capabilities
- Real-time inventory tracking
- Automatic credit limit enforcement
- Due date management for BNPL orders
- Payment prioritization (oldest orders first)
- Comprehensive user and order status reporting
- Robust error handling and validation

## System Architecture

```
BNPL System
├── BNPLSystem (Main Controller)
├── Data Models
│   ├── User (User information and credit management)
│   ├── Product (Product catalog)
│   ├── InventoryItem (Stock management)
│   └── Order (Order tracking and payment status)
└── Enums
    ├── PaymentMode (PREPAID/BNPL)
    └── OrderStatus (PLACED/PAID/DEFAULTED)
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd bnpl
```

2. No external dependencies required - uses only Python standard library

3. Run the demo:
```bash
python demo_test_cases.py
```

## Usage

### Basic Setup

```python
from bnpl import BNPLSystem
from data_models import Product, User, PaymentMode

# Initialize the system
system = BNPLSystem()

# Add products to inventory
product = Product("P001", "iPhone 15", "Electronics", 999.99, "Apple smartphone")
system.add_product_to_inventory(product, 10)

# Add users
user = User("U001", "Alice Johnson", 5000.0)  # user_id, name, credit_limit
system.add_user(user)

# Place orders
order_id = system.place_order("U001", "P001", 1, PaymentMode.BNPL)

# Clear dues
system.clear_dues("U001", 500.0)
```

### Key Methods

#### Inventory Management
```python
# Add product to inventory
system.add_product_to_inventory(product, quantity)

# Check inventory status
status = system.get_inventory_status()  # All products
status = system.get_inventory_status("P001")  # Specific product
```

#### User Management
```python
# Add user
system.add_user(user)

# Get user status
status = system.get_user_status("U001")

# Get user order history
history = system.get_user_order_history("U001")
```

#### Order Processing
```python
# Place order (returns order_id if successful, None if failed)
order_id = system.place_order(user_id, product_id, quantity, payment_mode)

# Clear user dues
success = system.clear_dues(user_id, amount)
```

## Data Models

### User
- `user_id`: Unique identifier
- `name`: User's name
- `credit_limit`: Maximum credit allowed
- `used_credit`: Currently used credit
- `is_blacklisted`: Blacklist status
- `default_count`: Number of defaults

### Product
- `product_id`: Unique identifier
- `name`: Product name
- `category`: Product category
- `price`: Product price
- `description`: Product description

### Order
- `order_id`: Unique identifier
- `user_id`: User who placed the order
- `product_id`: Ordered product
- `quantity`: Order quantity
- `total_amount`: Total order value
- `payment_mode`: PREPAID or BNPL
- `status`: PLACED, PAID, or DEFAULTED
- `due_date`: Payment due date (BNPL only)
- `amount_paid`: Amount already paid
- `remaining_amount`: Outstanding amount

## Business Rules

### Credit Management
- Users have a defined credit limit
- BNPL orders consume available credit
- Credit is released when payments are made
- Insufficient credit prevents BNPL orders

### Default Detection
- BNPL orders become defaulted when overdue
- System automatically checks and updates default status
- Default count is tracked per user

### Blacklisting
- Users with 3+ defaults are automatically blacklisted
- Blacklisted users cannot place BNPL orders
- Blacklisted users can still place prepaid orders

### Payment Processing
- Payments are applied to oldest orders first
- Partial payments are supported
- Orders are marked as PAID when fully settled
- Excess payments are noted but not applied

## Error Handling

The system includes comprehensive error handling for:
- Invalid user IDs
- Non-existent products
- Insufficient inventory
- Credit limit violations
- Invalid payment amounts
- Blacklisted user restrictions

## Example Scenarios

### Successful BNPL Purchase
```python
# User with sufficient credit buys a product
order_id = system.place_order("U001", "P001", 1, PaymentMode.BNPL)
# Order placed, credit consumed, due date set
```

### Credit Limit Exceeded
```python
# User tries to buy beyond credit limit
order_id = system.place_order("U001", "P002", 10, PaymentMode.BNPL)
# Returns None, prints insufficient credit message
```

### Payment and Credit Release
```python
# User makes payment
system.clear_dues("U001", 500.0)
# Payment applied to oldest orders, credit released
```

### Default and Blacklisting
```python
# System detects overdue payments
system.check_and_update_defaults("U001")
# Orders marked as defaulted, user may be blacklisted
```

## File Structure

```
bnpl/
├── README.md              # This file
├── bnpl.py               # Main BNPL system implementation
├── data_models.py        # Data models and enums
├── demo_test_cases.py    # Comprehensive demo and tests
└── .gitignore           # Git ignore file
```
