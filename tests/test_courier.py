import allure
import pytest
from api.courier import Courier
from conftest import created_courier


@allure.epic('Тестирование API аккаунта курьера сервиса "Yandex Самокат"')
class TestCreateCourier:
    @allure.title('Проверка регистрации курьера с корректными данными')
    def test_create_courier_success(self):
        courier = Courier()
        response = courier.create_courier()
        assert response.status_code == 201 and response.json() == {'ok': True}


    @allure.title('Проверка регистрации курьера с повторяющимися данными')
    def test_create_two_identical_couriers_failure(self, created_courier):
        response = created_courier.create_courier(
            created_courier.get_login(), created_courier.get_password(), created_courier.get_name())
        assert response.status_code == 409 and response.json().get(
            'message') == 'Этот логин уже используется. Попробуйте другой.'


    @allure.title('Проверка регистрации курьера с пустыми login или password')
    @pytest.mark.parametrize("key", ["login", "password"])
    def test_create_account_with_no_login_or_password_failed(self, key):
        courier = Courier()
        courier.create_courier()
        creds = courier.get_account_data()
        creds[key] = ''
        response = courier.create_courier(creds)
        assert response.status_code == 400 and response.json().get(
            'message') == 'Недостаточно данных для создания учетной записи'


    @allure.title('Проверка регистрации курьера с пустым name')
    def test_create_account_with_no_name_success(self):
        courier = Courier()
        courier.create_courier()
        creds = courier.get_account_data()
        creds['name'] = ''
        response = courier.create_courier(creds)
        assert (response.status_code == 409 and response.json().get('message') ==
                'Этот логин уже используется. Попробуйте другой.')


class TestLoginCourier:
    @allure.title('Проверка логина курьера с корректными данными')
    def test_login_courier_success(self, created_courier):
        response = created_courier.login_courier()
        created_courier.account_id = response.json().get('id')
        assert response.status_code == 200 and created_courier.account_id is not None


    @allure.title('Проверка логина курьера без обязательных полей login или password')
    @pytest.mark.parametrize("key", ("login", "password"))
    def test_login_without_necessary_field_failure(self, created_courier, key):
        created_courier.data[key] = ''
        response = created_courier.login_courier()
        assert response.status_code == 400 and response.json().get('message') == 'Недостаточно данных для входа'


    @allure.title('Проверка логина курьера с неверными login и password')
    @pytest.mark.parametrize("key", ("login", "password"))
    def test_login_with_wrong_credentials_failure(self, created_courier, key):
        created_courier.data[key] = 'Unknown'
        response = created_courier.login_courier()
        assert response.status_code == 404 and response.json().get('message') == 'Учетная запись не найдена'


class TestDeleteCourier:
    @allure.title('Проверка удаления курьера с корректным id')
    def test_delete_courier_success(self):
        courier = Courier()
        courier.create_courier()
        response = courier.delete_courier(courier.get_courier_id())
        assert response.status_code == 200 and response.json() == {'ok': True}


    # Ожидаемый status_code в тесте - 500, и тест падает (если courier_id='' - код 404).
    # Пожалуйста, подскажите, как быть и ожидаемо ли. Спасибо.
    @allure.title('Проверка удаления курьера с пустым id')
    def test_delete_courier_with_empty_id(self):
        courier = Courier()
        courier.create_courier()
        response = courier.delete_courier(courier_id=None)

        assert response.status_code == 400
        assert response.json()['message'] == 'Недостаточно данных для удаления курьера'


    @allure.title('Проверка удаления курьера с неверным id')
    def test_delete_courier_with_wrong_id(self):
        courier = Courier()
        response = courier.delete_courier(123)
        assert response.status_code == 404
        assert response.json()['message'] == 'Курьера с таким id нет.'
