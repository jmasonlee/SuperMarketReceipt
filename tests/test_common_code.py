import pytest
from approvaltests import verify

from model_objects import Product, ProductUnit
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog


def test_common_code_empty_catalog():
    teller = Teller(FakeCatalog())
    verify(teller.common_code(ShoppingCart()))


def test_item_not_in_catalog():
    teller = Teller(FakeCatalog())

    cart = ShoppingCart()
    cart.add_item(Product("toothbrush", ProductUnit.EACH))

    with pytest.raises(KeyError) as exception:
        teller.common_code(cart)
    verify(exception)

#catalog with toothbrush and apples, checkout toothbrush and apples
#catalog with toothbrush and apples, checkout apples
