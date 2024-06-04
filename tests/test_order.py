import allure
import pytest
import logging

from api.order import Order
from conftest import created_courier
import helpers.utils as helper

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@allure.epic('Тестирование API заказа самоката сервиса "Yandex Самокат"')
class TestOrder:
    @allure.title('Проверка создания заказа с корректными данными')
    @pytest.mark.parametrize('color', (['BLACK'], ['GREY'], ['BLACK', 'GREY'], ''))
    def test_create_order_success(self, color: list):
        order = Order()
        order_data = helper.generate_order_data(color)
        response = order.create_order(order_data)
        assert response.status_code == 201 and 'track' in response.json()


    @allure.title('Получить список заказов')
    def test_get_list_of_orders(self):
        response = Order.get_list_of_orders()
        assert response.status_code == 200


    @allure.title('Принять заказ курьером')
    def test_accept_order_success(self, created_courier):
        order = Order()
        order_data = helper.generate_order_data(['BLACK'])
        response = order.create_order(order_data)

        order_id = order.get_order_id()
        courier_id = created_courier.get_courier_id()

        response = order.accept_order(order_id, courier_id)
        assert response.status_code == 200 and response.json() == {'ok': True}


    @allure.title('Принять заказ курьером с несуществующим id заказа')
    def test_accept_order_nonexistent_order_id_failure(self, created_courier):
        order = Order()
        order_data = helper.generate_order_data(['BLACK'])
        order.create_order(order_data)

        courier_id = created_courier.get_courier_id()
        order_id = 111111111

        response = order.accept_order(order_id=order_id, courier_id=courier_id)
        assert response.status_code == 404 and response.json()['message'] == "Заказа с таким id не существует"


    @allure.title('Принять заказ с несуществующим id курьера')
    def test_accept_order_nonexistent_courier_id_failure(self, created_courier):
        order = Order()
        order_data = helper.generate_order_data(['BLACK'])
        order.create_order(order_data)

        courier_id = 111111111
        order_id = order.get_order_track_num()

        response = order.accept_order(order_id, courier_id)
        assert response.status_code == 404 and response.json()['message'] == "Курьера с таким id не существует"


    @allure.title('Принять заказ курьером с пустым id заказа')
    def test_accept_order_empty_courier_id_failure(self, created_courier):
        order = Order()
        order_data = helper.generate_order_data(['BLACK'])
        order.create_order(order_data)

        courier_id = created_courier.get_courier_id()
        order_id = ''

        response = order.accept_order(order_id, courier_id)
        assert response.status_code == 400 and response.json()['message'] == "Недостаточно данных для поиска"


    @allure.title('Принять заказ с пустым id курьера')
    def test_accept_order_empty_courier_id_failure(self, created_courier):
        order = Order()
        order_data = helper.generate_order_data(['BLACK'])
        order.create_order(order_data)

        courier_id = ''
        order_id = order.get_order_id()

        response = order.accept_order(order_id, courier_id)
        assert response.status_code == 400 and response.json()['message'] == "Недостаточно данных для поиска"


    @allure.title('Принять заказ, который уже был в работе')
    def test_accept_order_had_been_in_work_failure(self, created_courier):
        order = Order()
        order_data = helper.generate_order_data(['BLACK'])
        order.create_order(order_data)

        courier_id = created_courier.get_courier_id()
        order_id = 100

        response = order.accept_order(order_id, courier_id)
        assert response.status_code == 409 and response.json()['message'] == "Этот заказ уже в работе"


    @allure.title('Найти данные заказа по id заказа')
    def test_get_order_by_id_success(self):
        order = Order()
        order_data = helper.generate_order_data(['BLACK'])
        order.create_order(order_data)
        order_id = order.get_order_id()

        response = order.get_order_by_track_num(order_id)
        assert response.status_code == 200 and 'order' in response.json()


    @allure.title('Найти данные заказа по пустому id заказа')
    def test_get_order_with_no_id_failure(self):
        response = Order().get_order_by_track_num('')
        assert response.status_code == 400 and response.json()['message'] == 'Недостаточно данных для поиска'


    @allure.title('Найти данные заказа по несуществующему id заказа')
    def test_get_order_with_no_id_failure(self):
        response = Order().get_order_by_track_num(1)
        assert response.status_code == 404 and response.json()['message'] == 'Заказ не найден'
