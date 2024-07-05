import pytest

from api.courier import Courier


@pytest.fixture(scope='function')
def created_courier():
    courier = Courier()
    courier.create_courier()
    yield courier
    courier.delete_courier(courier.get_courier_id())


@pytest.fixture(scope='function')
def courier_delete_after_use():
    courier = None
    yield courier
    if courier:
        courier.delete_courier(courier.get_courier_id())
