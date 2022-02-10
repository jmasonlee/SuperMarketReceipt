from model_objects import Offer
from receipt import Receipt


class Teller:

    def __init__(self, catalog):
        self.catalog = catalog
        self.offers = {}

    def add_special_offer(self, offer_type, product, argument):
        self.offers[product] = Offer(offer_type, product, argument)

    def checks_out_articles_from(self, the_cart, receipt=None):
        #Begin Common Code
        # receipt = self.calculate_total_charges(the_cart)
        assert receipt is not None

        expected_receipt = Receipt()
        for item in the_cart.items:
            expected_receipt.add_product(item.product, item.quantity, self.catalog.unit_price(item.product), item.quantity * self.catalog.unit_price(item.product))
        assert str(receipt.items) == str(expected_receipt.items)
        ### EXIT CRITERION: receipt is not present
        ### EXIT CRITERION: receipt needs to have values for the items being purchased
        #End Common Code Note: handle_offers could also contain common code

        the_cart.handle_offers(receipt, self.offers, self.catalog)

        return receipt

    def calculate_total_charges(self, the_cart):
        receipt = Receipt()
        product_quantities = the_cart.items
        for pq in product_quantities:
            p = pq.product
            quantity = pq.quantity
            unit_price = self.catalog.unit_price(p)
            price = quantity * unit_price
            # price = 0.00 #quantity * unit_price
            receipt.add_product(p, quantity, unit_price, price)
        return receipt
