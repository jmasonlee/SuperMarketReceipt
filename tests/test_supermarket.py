import pytest

from model_objects import Product, SpecialOfferType, ProductUnit, Discount
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog
from approvaltests import verify


def test_ten_percent_discount():
    apples, teller, toothbrush = create_teller_and_items()
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)

    cart = ShoppingCart()
    cart.add_item_quantity(apples, 2.5)
    cart.add_item_quantity(toothbrush, 1)

    receipt = teller.checks_out_articles_from(cart)

    verify(str(receipt))


def test_full_receipt_no_discount():
    apples, teller, toothbrush = create_teller_and_items()

    cart = ShoppingCart()
    cart.add_item_quantity(apples, 2.5)
    cart.add_item_quantity(toothbrush, 1)

    receipt = teller.checks_out_articles_from(cart)

    verify(str(receipt))


def test_full_receipt_add_item_adds_one_item():
    apples, teller, toothbrush = create_teller_and_items()

    cart = ShoppingCart()
    cart.add_item(apples)
    cart.add_item(toothbrush)

    receipt = teller.checks_out_articles_from(cart)

    verify(str(receipt))


def test_product_quantities_updates():
    apples, teller, toothbrush = create_teller_and_items()

    cart = ShoppingCart()
    cart.add_item(apples)
    cart.add_item_quantity(toothbrush, 2.0)
    cart.add_item(toothbrush)

    receipt = teller.checks_out_articles_from(cart)
    verify(str(cart.product_quantities) + str(receipt))


def test_full_receipt_three_for_two():
    apples, teller, toothbrush = create_teller_and_items()
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, "foor")

    cart = ShoppingCart()
    cart.add_item_quantity(apples, 2.5)
    cart.add_item_quantity(toothbrush, 1)

    receipt = teller.checks_out_articles_from(cart)

    verify(str(receipt))


def create_teller_and_items():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)
    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 1.99)
    teller = Teller(catalog)
    return apples, teller, toothbrush
