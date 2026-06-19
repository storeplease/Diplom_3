import allure
from pages.main_page import MainPage
from pages.login_page import LoginPage
from helpers import Helpers
from urls import FORGOT_PASSWORD_URL


class TestPasswordRecovery:

    @allure.title('Переход на страницу восстановления пароля по кнопке «Восстановить пароль»')
    @allure.description('Проверка перехода на страницу forgot-password по клику на ссылку "Восстановить пароль"')
    @allure.feature('Восстановление пароля')
    def test_go_to_restore_password(self, driver):
        main_page = MainPage(driver)
        login_page = LoginPage(driver)

        main_page.click_personal_account()
        login_page.click_restore_password_link()

        current_url = login_page.get_current_url()
        assert FORGOT_PASSWORD_URL in current_url, (
            f"Ожидался URL {FORGOT_PASSWORD_URL}, получен {current_url}"
        )

    @allure.title('Ввод почты и клик по кнопке «Восстановить»')
    @allure.description('Проверка, что после ввода email и клика по кнопке открывается форма сброса пароля')
    @allure.feature('Восстановление пароля')
    def test_restore_password_process(self, driver, registered_user):
        main_page = MainPage(driver)
        login_page = LoginPage(driver)

        payload, access_token = registered_user
        email = payload['email']

        main_page.click_personal_account()
        login_page.click_restore_password_link()

        login_page.enter_restore_email(email)
        login_page.click_restore_button()

        assert login_page.is_on_reset_password_page(), (
            "Форма сброса пароля не открылась после отправки email"
        )

    @allure.title('Клик по кнопке показать/скрыть пароль делает поле активным')
    @allure.description('Проверка, что после клика на глазик поле пароля подсвечивается (становится активным)')
    @allure.feature('Восстановление пароля')
    def test_toggle_password_visibility(self, driver, registered_user):
        main_page = MainPage(driver)
        login_page = LoginPage(driver)

        payload, access_token = registered_user
        email = payload['email']

        main_page.click_personal_account()
        login_page.click_restore_password_link()

        login_page.enter_restore_email(email)
        login_page.click_restore_button()

        password = Helpers.generate_password()
        login_page.enter_password_to_passive_field(password)
        login_page.click_toggle_password_visibility()

        assert login_page.is_active_password_field_displayed(), (
            "Поле пароля не стало активным после клика по кнопке показать/скрыть"
        )
