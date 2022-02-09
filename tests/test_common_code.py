from approvaltests import verify

from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog


def test_common_code_empty_catalog():
    teller = Teller(FakeCatalog())
    verify(teller.common_code(ShoppingCart()))
