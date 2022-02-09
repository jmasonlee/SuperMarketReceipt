import pytest
from approvaltests import verify

from model_objects import Product, ProductUnit
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog


def test_common_code_empty_catalog():
    teller = Teller(FakeCatalog())
    verify(teller.calculate_total_charges(ShoppingCart()))


def test_item_not_in_catalog():
    teller = Teller(FakeCatalog())

    cart = ShoppingCart()
    cart.add_item(Product("toothbrush", ProductUnit.EACH))

    with pytest.raises(KeyError) as exception:
        teller.calculate_total_charges(cart)
    verify(exception)


def test_checkout_everything_in_the_catalog():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    apple = Product("apple", ProductUnit.KILO)
    catalog.add_product(toothbrush, 2.00)
    catalog.add_product(apple, 1.50)

    teller = Teller(catalog)

    cart = ShoppingCart()
    cart.add_item(toothbrush)
    cart.add_item(apple)

    verify(teller.calculate_total_charges(cart))


def test_checkout_one_item_from_catalog():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    apple = Product("apple", ProductUnit.KILO)
    catalog.add_product(toothbrush, 2.00)
    catalog.add_product(apple, 1.50)

    teller = Teller(catalog)

    cart = ShoppingCart()
    cart.add_item(toothbrush)

    verify(teller.calculate_total_charges(cart))
