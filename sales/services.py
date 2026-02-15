from django.shortcuts import get_object_or_404, get_list_or_404
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from payments.models import PaymentMethod, Payment
from inventory.models import Stock, Product, StockMovement
from inventory.services import apply_stock_movement
from accounts.models import Branch
from customers.models import Customer, CustomerAddress
from django.db import transaction
from sales.models import Sale, SaleItem

@transaction.atomic
def create_sale(cart_data, post_data, user):
    if not cart_data:
        raise ValueError("Your cart is empty")

    discount_amount = Decimal(post_data['discount_amount']) or 0
    cart_total = sum(
        Decimal(item["total"])
        for item in cart_data.values()
    )
    
    payable_amount = cart_total - discount_amount
    payment_amounts = post_data.getlist("payment_amount[]")
    payment_methods = post_data.getlist("payment_method[]")
    payment_notes = post_data.getlist("payment_note[]")

    if not payment_amounts:
        raise ValueError("At least one payment is required")

    payments = []
    total_payment = Decimal("0.00")

    for amount, method, note in zip(payment_amounts, payment_methods, payment_notes):
        if not amount or not method:
            continue

        try:
            amount = Decimal(amount)
        except InvalidOperation:
            continue
        
        if amount <= 0:
            continue
        
        payments.append({
            'payment_method': PaymentMethod.objects.get(pk=method),
            "method": method,
            "amount": amount,
            "notes": note or ""
        })

        total_payment += amount
    
    if not payments:
        raise ValueError("Valid payment information is required")

    if total_payment < payable_amount:
        raise ValueError(
            f"Insufficient payment. Required: {payable_amount}, Paid: {total_payment}"
        )
    
    # Get Branch
    branch = get_object_or_404(Branch, pk=post_data['branch'])
    
    # Create Customer & CustomerAddress
    customer, _ = Customer.objects.get_or_create(
        phone=post_data['phone'], 
        defaults={'name':post_data.get('name',''), 'email':post_data.get('email', ''), 'loyalty_points':0}
    )
    if post_data.get('address'):
        CustomerAddress.objects.get_or_create(
            customer=customer,
            address=post_data['address'],
            defaults={'is_default':True}
        )
    
    # Create Sale
    sale = Sale.objects.create(
        branch=branch,
        cashier=user,
        customer=customer,
        subtotal=cart_total,
        tax_amount=0,
        discount_amount=discount_amount,
        total_amount=cart_total,
        status='DRAFT',
        notes=post_data.get('notes', ''),
    )

    subtotal = Decimal("0.00")
    total_tax = Decimal("0.00")
    for item in cart_data.values():
        product = Product.objects.select_for_update().get(pk=item['id'])

        if not product:
            continue
        
        # Stock lock and validation
        stock, _ = Stock.objects.select_for_update().get_or_create(
            product=product,
            branch=branch,
            defaults={'quantity': 0, 'reorder_level': 1}
        )

        qty = Decimal(item['quantity'])
        unit_price = Decimal(item['price'])

        if stock.quantity < qty:
            raise ValueError(f'Insufficient stock for product {item['name']} at branch {branch.name}')
        
        # Calculation
        item_subtotal = unit_price * qty
        tax_rate = Decimal(item['tax_rate'] or 0)
        tax_amount = (item_subtotal * tax_rate / 100).quantize(Decimal("0.01"))
        total_price = item_subtotal + tax_amount

        # Create SaleItem
        SaleItem.objects.create(
            sale=sale,
            product=product,
            quantity=qty,
            unit_price=unit_price,
            tax_rate=tax_rate,
            tax_amount=tax_amount,
            total_price=total_price,
        )

        # Create StockMovement (OUT)
        movement = StockMovement.objects.create(
            product=product,
            branch=branch,
            movement_type="OUT",
            quantity=qty,
            reference=f"SALE:{sale.id}",
            created_by=user,
        )

        apply_stock_movement(movement, user)

        subtotal += item_subtotal
        total_tax += tax_amount
    
    # Final Sale Totals
    sale.receipt_number = sale.id
    sale.subtotal = subtotal
    sale.tax_amount = total_tax
    sale.discount_amount = discount_amount
    sale.total_amount = subtotal + total_tax - discount_amount
    sale.status = 'COMPLETED'
    sale.save()

    # Create Payment
    for payment in payments:
        pay = Payment.objects.create(
            sale=sale,
            method=payment.get('payment_method'),
            amount=payment.get('amount'),
            status='pending',
            notes=payment.get('notes'),
            processed_by=user,
        )

        pay.number = pay.id
        pay.status = 'completed'
        pay.save()

    return sale
