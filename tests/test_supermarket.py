import pytest

from model_objects import Product, SpecialOfferType, ProductUnit, Discount
from receipt import Receipt
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

    receipt = Receipt()
    receipt.add_product(apples, 2.5, 1.99, 4.975)
    receipt.add_product(toothbrush, 1, 0.99, 0.99)

    receipt = teller.checks_out_articles_from(cart, receipt)

    verify(str(receipt))


def test_full_receipt_no_discount():
    apples, teller, toothbrush = create_teller_and_items()

    cart = ShoppingCart()
    cart.add_item_quantity(apples, 2.5)
    cart.add_item_quantity(toothbrush, 1)

    receipt = Receipt()
    receipt.add_product(apples, 2.5, 1.99, 4.975)
    receipt.add_product(toothbrush, 1, 0.99, 0.99)

    receipt = teller.checks_out_articles_from(cart, receipt)

    verify(str(receipt))


def test_full_receipt_add_item_adds_one_item():
    apples, teller, toothbrush = create_teller_and_items()

    cart = ShoppingCart()
    cart.add_item(apples)
    cart.add_item(toothbrush)

    receipt = Receipt()
    receipt.add_product(apples, 1.0, 1.99, 1.99)
    receipt.add_product(toothbrush, 1.0, 0.99, 0.99)

    receipt = teller.checks_out_articles_from(cart, receipt)

    verify(str(receipt))


def test_product_quantities_updates():
    apples, teller, toothbrush = create_teller_and_items()

    cart = ShoppingCart()
    cart.add_item(apples)
    cart.add_item_quantity(toothbrush, 2.0)
    cart.add_item(toothbrush)

    receipt = Receipt()
    receipt.add_product(apples, 1.0, 1.99, 1.99)
    receipt.add_product(toothbrush, 2.0, 0.99, 1.98)
    receipt.add_product(toothbrush, 1.0, 0.99, 0.99)

    receipt = teller.checks_out_articles_from(cart, receipt)
    verify(str(cart.product_quantities) + str(receipt))


def test_full_receipt_three_for_two():
    apples, teller, toothbrush = create_teller_and_items()
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, "foor")

    cart = ShoppingCart()
    cart.add_item_quantity(apples, 2.5)
    cart.add_item_quantity(toothbrush, 1)

    receipt = teller.checks_out_articles_from(cart)

    verify(str(receipt))


def test_full_receipt_two_for_one():
    apples, teller, toothbrush = create_teller_and_items()
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, apples, 1)

    cart = ShoppingCart()
    cart.add_item_quantity(apples, 2.5)
    cart.add_item_quantity(toothbrush, 1)

    receipt = Receipt()
    receipt.add_product(apples, 2.5, 1.99, 4.975)
    receipt.add_product(toothbrush, 1, 0.99, 0.99)

    receipt = teller.checks_out_articles_from(cart, receipt)

    verify(str(receipt))


def test_full_receipt_two_for_three():
    apples, teller, toothbrush = create_teller_and_items()
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, apples, 3)

    cart = ShoppingCart()
    cart.add_item_quantity(apples, 2.5)
    cart.add_item_quantity(toothbrush, 1)

    receipt = teller.checks_out_articles_from(cart)

    verify(str(receipt))


def test_full_receipt_two_for_one_one_item():
    apples, teller, toothbrush = create_teller_and_items()
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, apples, 1)

    cart = ShoppingCart()
    cart.add_item_quantity(apples, 1)
    cart.add_item_quantity(toothbrush, 1)

    receipt = teller.checks_out_articles_from(cart)

    verify(str(receipt))


def test_full_receipt_five_for_one():
    apples, teller, toothbrush = create_teller_and_items()
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, apples, 1)

    cart = ShoppingCart()
    cart.add_item_quantity(apples, 5)
    cart.add_item_quantity(toothbrush, 1)

    receipt = teller.checks_out_articles_from(cart)

    verify(str(receipt))


def test_full_receipt_three_for_two_more_than_two_items():
    apples, teller, toothbrush = create_teller_and_items()
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, apples, "foo")

    cart = ShoppingCart()
    cart.add_item_quantity(apples, 3)
    cart.add_item_quantity(toothbrush, 1)
    receipt = teller.checks_out_articles_from(cart)

    verify(str(receipt))


def test_full_receipt_five_for_amount_less_than_five_items():
    apples, teller, toothbrush = create_teller_and_items()
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, apples, "foo")

    cart = ShoppingCart()
    cart.add_item_quantity(apples, 3)
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
