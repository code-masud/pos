from decimal import Decimal, ROUND_HALF_UP


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get("cart", {})

    def _to_decimal(self, value):
        return Decimal(str(value))

    def _calculate_item_total(self, item):
        price = self._to_decimal(item["price"])
        qty = self._to_decimal(item["quantity"])
        tax_rate = self._to_decimal(item.get("tax_rate", "0"))

        if tax_rate > 0:
            tax_amount = (price * tax_rate) / Decimal("100")
            price += tax_amount

        return (price * qty).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def add(self, id, name, price, qty=1, tax_rate=0):
        product_id = str(id)
        qty = self._to_decimal(qty)

        if product_id not in self.cart:
            self.cart[product_id] = {
                "id": id,
                "name": name,
                "price": str(price),
                "quantity": "0",
                "tax_rate": str(tax_rate),
            }

        current_qty = self._to_decimal(self.cart[product_id]["quantity"])
        self.cart[product_id]["quantity"] = str(current_qty + qty)
        self.cart[product_id]["total"] = str(self._calculate_item_total(self.cart[product_id]))

        self.save()

    def update(self, product_id, quantity):
        product_id = str(product_id)

        if product_id in self.cart:
            quantity = self._to_decimal(quantity)

            if quantity <= 0:
                self.remove(product_id)
            else:
                self.cart[product_id]["quantity"] = str(quantity)

            self.cart[product_id]["total"] = str(self._calculate_item_total(self.cart[product_id]))
            self.save()

    def increment(self, product_id, quantity=1):
        product_id = str(product_id)
        self.add(product_id,
                 self.cart[product_id]["name"],
                 self.cart[product_id]["price"],
                 quantity,
                 self.cart[product_id]["tax_rate"])

    def decrement(self, product_id, quantity=1):
        product_id = str(product_id)

        if product_id in self.cart:
            current_qty = self._to_decimal(self.cart[product_id]["quantity"])
            new_qty = current_qty - self._to_decimal(quantity)

            if new_qty <= 0:
                self.remove(product_id)
            else:
                self.cart[product_id]["quantity"] = str(new_qty)
                self.cart[product_id]["total"] = str(self._calculate_item_total(self.cart[product_id]))
                self.save()

    def remove(self, product_id):
        product_id = str(product_id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def total(self):
        total = sum(
            self._calculate_item_total(item)
            for item in self.cart.values()
        )
        return Decimal(total).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def total_qty(self):
        return sum(
            self._to_decimal(item["quantity"])
            for item in self.cart.values()
        )

    def save(self):
        self.session["cart"] = self.cart
        self.session.modified = True

    def clear(self):
        self.session.pop("cart", None)
        self.session.modified = True