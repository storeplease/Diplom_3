import allure
from locators.main_page_locators import MainPageLocators
from pages.base_page import BasePage
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from data import INGREDIENT_NAMES
from urls import BASE_URL


class MainPage(BasePage):

    @allure.step("Нажать на кнопку «Конструктор»")
    def click_constructor(self):
        self.click_to_element(MainPageLocators.CONSTRUCTOR_BUTTON)

    @allure.step("Нажать на ссылку «Лента заказов»")
    def click_order_feed(self):
        self.click_to_element(MainPageLocators.ORDER_FEED_LINK)

    @allure.step("Нажать на «Личный кабинет»")
    def click_personal_account(self):
        self.click_to_element(MainPageLocators.PERSONAL_ACCOUNT_BUTTON)
        try:
            self.wait_for_url_contains('/account', time=5)
        except Exception:
            self.go_to_url(f"{BASE_URL}account")

    @allure.step("Кликнуть на ингредиент")
    def click_ingredient(self, index=0):
        self._dismiss_overlay_if_present()
        ingredients = self.find_elements(MainPageLocators.INGREDIENT)
        try:
            ingredients[index].click()
        except ElementClickInterceptedException:
            self.click_using_js(ingredients[index])

    @allure.step("Добавить ингредиент в заказ")
    def add_ingredient_to_order(self, index=0):
        ingredient = self.find_elements(MainPageLocators.INGREDIENT)[index]
        name = INGREDIENT_NAMES.get(index, str(index))
        with allure.step(f"Перетащить {name} в корзину"):
            target = self.find_element_with_wait(MainPageLocators.TARGET_AREA)
            self.drag_and_drop(ingredient, target)

    @allure.step("Проверить видимость модального окна ингредиента")
    def is_ingredient_modal_visible(self):
        return self.is_displayed(MainPageLocators.MODAL_WINDOW)

    @allure.step("Проверить, что модальное окно закрыто")
    def is_ingredient_modal_closed(self):
        try:
            self.wait_element_until_invisibility(MainPageLocators.MODAL_WINDOW, time=5)
            return True
        except TimeoutException:
            return False

    @allure.step("Закрыть модальное окно ингредиента")
    def close_ingredient_modal(self):
        self.close_modal_with_overlay(
            MainPageLocators.MODAL_WINDOW,
            MainPageLocators.CLOSE_MODAL_BUTTON,
            MainPageLocators.MODAL_OVERLAY
        )

    @allure.step("Получить значение счётчика ингредиента")
    def get_ingredient_counter(self, index=0):
        try:
            counters = self.find_elements(MainPageLocators.INGREDIENT_COUNTER)
            return int(counters[index].text.strip())
        except (TimeoutException, NoSuchElementException, ValueError, IndexError):
            return 0

    @allure.step("Дождаться увеличения счётчика ингредиента")
    def wait_for_counter_change(self, index, initial_value, timeout=10):
        def _counter_updated(driver):
            return self.get_ingredient_counter(index=index) > initial_value
        self.wait_for_condition(_counter_updated, timeout)

    @allure.step("Нажать кнопку «Оформить заказ»")
    def click_order_button(self):
        self.click_to_element(MainPageLocators.ORDER_BUTTON)

    @allure.step("Проверить видимость модального окна заказа")
    def is_order_modal_visible(self):
        return self.is_displayed(MainPageLocators.ORDER_MODAL_CONTAINER)

    @allure.step("Закрыть модальное окно заказа")
    def close_order_modal(self):
        self.close_modal_with_overlay(
            MainPageLocators.ORDER_MODAL_CONTAINER,
            MainPageLocators.CLOSE_ORDER_MODAL_BUTTON,
            MainPageLocators.MODAL_OVERLAY
        )

    @allure.step("Проверить отображение конструктора")
    def is_constructor_displayed(self):
        return self.is_displayed(MainPageLocators.TARGET_AREA)

    @allure.step("Получить номер заказа из модалки")
    def get_order_number_from_modal(self):
        return self.get_order_number(MainPageLocators.ORDER_NUMBER)

    @allure.step("Логин пользователя")
    def login_user(self, email, password):
        from pages.login_page import LoginPage
        self.click_personal_account()
        login_page = LoginPage(self.driver)
        login_page.enter_login_email(email)
        login_page.enter_login_password(password)
        login_page.click_login_button()
        self.wait_for_url_contains(BASE_URL, 10)
