import pytest

from api.courier import Courier


@pytest.fixture(scope='function')
def created_courier():
    courier = Courier()
    try:
        courier.create_courier()
    except Exception as e:
        raise RuntimeError("Failed to create courier") from e

    yield courier

    try:
        courier.delete_courier(courier.get_courier_id())
    except Exception as e:
        raise RuntimeError("Failed to delete courier") from e
