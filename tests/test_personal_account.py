import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage
from pages.login_page import LoginPage
from urls import BASE_URL, LOGIN_URL


class TestPersonalAccount:

    def _login_and_wait(self, driver, email, password):
        main_page = MainPage(driver)
        login_page = LoginPage(driver)

        main_page.click_personal_account()
        login_page.enter_login_email(email)
        login_page.enter_login_password(password)
        login_page.click_login_button()

        WebDriverWait(driver, 10).until(EC.url_contains(BASE_URL))

    @allure.title('Переход по клику на «Личный кабинет»')
    @allure.description('Проверка, что авторизованный пользователь может перейти в личный кабинет')
    @allure.feature('Личный кабинет')
    def test_go_to_personal_account(self, driver, registered_user):
        main_page = MainPage(driver)

        payload, access_token = registered_user
        self._login_and_wait(driver, payload['email'], payload['password'])

        main_page.click_personal_account()
        WebDriverWait(driver, 10).until(EC.url_contains('/account'))
        current_url = main_page.get_current_url()
        assert '/account' in current_url, (
            f"Ожидался URL, содержащий /account, получен {current_url}"
        )

    @allure.title('Переход в раздел «История заказов»')
    @allure.description('Проверка, что в личном кабинете можно перейти в историю заказов')
    @allure.feature('Личный кабинет')
    def test_go_to_order_history(self, driver, registered_user):
        main_page = MainPage(driver)
        login_page = LoginPage(driver)

        payload, access_token = registered_user
        self._login_and_wait(driver, payload['email'], payload['password'])

        main_page.click_personal_account()
        WebDriverWait(driver, 10).until(EC.url_contains('/account'))
        login_page.click_order_history()

        current_url = login_page.get_current_url()
        assert '/account/order-history' in current_url, (
            f"Не удалось перейти в историю заказов. Текущий URL: {current_url}"
        )

    @allure.title('Выход из аккаунта')
    @allure.description('Проверка, что пользователь может выйти из личного кабинета')
    @allure.feature('Личный кабинет')
    def test_logout(self, driver, registered_user):
        main_page = MainPage(driver)
        login_page = LoginPage(driver)

        payload, access_token = registered_user
        self._login_and_wait(driver, payload['email'], payload['password'])

        main_page.click_personal_account()
        WebDriverWait(driver, 10).until(EC.url_contains('/account'))
        login_page.click_logout_button()
        WebDriverWait(driver, 10).until(EC.url_to_be(LOGIN_URL))

        current_url = login_page.get_current_url()
        assert LOGIN_URL in current_url, (
            f"Выход не выполнен. Текущий URL: {current_url}"
        )
