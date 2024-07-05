import allure
import logging
import requests

import helpers.urls as url

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class Order:

    def __init__(self):
        self.track_num = None
        self.id = None
        self.data = {}


    @allure.step('Создание заказа')
    def create_order(self, data):
        url_create_order = f"{url.BASE_URL}{url.CREATE_ORDER}"
        logger.debug(f"POST create order with data: {data}, URL: {url_create_order}")

        response = requests.post(url_create_order, json=data)

        self.track_num = response.json()['track']
        self.data = self.get_order_by_track_num(self.track_num)
        self.id = self.get_order_id_by_track_num(self.data)

        return response


    @staticmethod
    @allure.step('Получение списка заказов')
    def get_list_of_orders():
        return requests.get(url.BASE_URL + url.ORDER_LIST)


    @allure.step('Принятие заказа курьером')
    def accept_order(self, order_id: int = None, courier_id: int = None):
        url_accept_order = f"{url.BASE_URL}{url.ACCEPT_ORDER}/{order_id}?courierId={courier_id}"
        logger.debug(f"PUT request to accept order, URL: {url_accept_order}")
        return requests.put(url_accept_order, timeout=30)


    @allure.step('Отмена заказа')
    def cancel_order(self, order_id: int = None):
        url_cancel_order = f"{url.BASE_URL}{url.CANCEL_ORDER}/{order_id}"
        data = {'track': order_id}
        logger.debug(f"PUT request to cancel order, URL: {url_cancel_order}, data: {data}")
        return requests.put(url_cancel_order, data=data)

    @allure.step('Получение заказа по номеру')
    def get_order_by_track_num(self, order_track_num: int = None):
        return requests.get(f"{url.BASE_URL}{url.GET_ORDER_BY_ID}?t={order_track_num}")


    @allure.step('Получение id заказа по номеру')
    def get_order_id_by_track_num(self, data):
        return data.json()['order']['id']


    @allure.step('Получение id заказа')
    def get_order_id(self):
        if self.id:
            return self.id
        return None


    @allure.step('Получить трек-номер заказа')
    def get_order_track_num(self):
        if self.track_num:
            return self.track_num
        return None
