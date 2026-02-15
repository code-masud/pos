from django.db import transaction
from inventory.models import Stock, StockMovement

@transaction.atomic
def apply_stock_movement(movement, user):
    
    stock, _ = Stock.objects.select_for_update().get_or_create(
        product=movement.product,
        branch=movement.branch,
        defaults={"quantity": 0, "reorder_level": 5}
    )

    if movement.movement_type == StockMovement.IN:
        stock.quantity += movement.quantity

    elif movement.movement_type == StockMovement.OUT:
        if stock.quantity < movement.quantity:
            raise ValueError("Insufficient stock")
        stock.quantity -= movement.quantity

    elif movement.movement_type == StockMovement.ADJUSTMENT:
        stock.quantity += movement.quantity

    stock.save()

    movement.created_by = user
    movement.save()