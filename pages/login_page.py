import allure
from locators.login_locators import LoginLocators
from pages.base_page import BasePage
from urls import RESET_PASSWORD_URL

class LoginPage(BasePage):

    @allure.step("Ввести email для входа")
    def enter_login_email(self, email):
        self.input_text(LoginLocators.LOGIN_EMAIL_INPUT, email)

    @allure.step("Ввести пароль для входа")
    def enter_login_password(self, password):
        self.input_text(LoginLocators.LOGIN_PASSWORD_INPUT, password)

    @allure.step("Нажать кнопку «Войти»")
    def click_login_button(self):
        self.click_to_element(LoginLocators.LOGIN_BUTTON)

    @allure.step("Нажать ссылку «Восстановить пароль»")
    def click_restore_password_link(self):
        self.click_to_element(LoginLocators.RESTORE_PASSWORD_LINK)

    @allure.step("Ввести email для восстановления пароля")
    def enter_restore_email(self, email):
        self.input_text(LoginLocators.RESTORE_EMAIL_INPUT, email)

    @allure.step("Нажать кнопку «Восстановить»")
    def click_restore_button(self):
        self.click_to_element(LoginLocators.RESTORE_BUTTON)

    @allure.step("Проверить, что открыта форма сброса пароля")
    def is_on_reset_password_page(self):
        current_url = self.get_current_url()
        if RESET_PASSWORD_URL in current_url:
            return True
        return self.is_displayed(LoginLocators.PASSWORD_FIELD_PASSIVE)

    @allure.step("Ввести пароль в скрытое поле (пассивное состояние)")
    def enter_password_to_passive_field(self, password):
        self.input_text(LoginLocators.PASSWORD_FIELD_PASSIVE, password)

    @allure.step("Кликнуть по кнопке показать/скрыть пароль")
    def click_toggle_password_visibility(self):
        self.click_to_element(LoginLocators.TOGGLE_PASSWORD_VISIBILITY)

    @allure.step("Проверить, что активное поле пароля отображается")
    def is_active_password_field_displayed(self):
        return self.is_displayed(LoginLocators.PASSWORD_FIELD_ACTIVE)

    @allure.step("Нажать кнопку «Выход»")
    def click_logout_button(self):
        self.click_to_element(LoginLocators.LOGOUT_BUTTON)

    @allure.step("Нажать «История заказов» в личном кабинете")
    def click_order_history(self):
        self.click_to_element(LoginLocators.ORDER_HISTORY_LINK)


