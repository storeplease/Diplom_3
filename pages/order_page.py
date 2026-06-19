import allure
from locators.order_locators import OrderLocators
from pages.base_page import BasePage
from selenium.common.exceptions import TimeoutException


class OrderPage(BasePage):

    @allure.step("Нажать на заказ в ленте заказов")
    def click_order_feed_item(self, index=0):
        items = self.find_elements(OrderLocators.ORDER_FEED_ITEM)
        items[index].click()

    @allure.step("Проверить, что детали заказа открылись")
    def is_order_details_visible(self):
        has_modal = self.is_displayed(OrderLocators.ORDER_DETAILS_MODAL)
        has_feed_url = '/feed/' in self.get_current_url() and len(self.get_current_url()) > len('/feed/')
        return has_modal or has_feed_url

    @allure.step("Получить список заказов в ленте")
    def get_order_feed_items(self):
        elements = self.find_elements(OrderLocators.ORDER_FEED_ITEM)
        return [el.text for el in elements]

    @allure.step("Проверить отображение ленты заказов")
    def is_feed_displayed(self):
        return self.is_displayed(OrderLocators.ORDER_FEED_LIST)

    @allure.step("Дождаться загрузки ленты заказов")
    def wait_for_order_feed(self):
        self.wait_element_until_visibility(OrderLocators.ORDER_FEED_LIST)

    @allure.step("Дождаться загрузки истории заказов")
    def wait_for_order_history(self):
        self.wait_element_until_visibility(OrderLocators.ORDER_HISTORY_LIST)

    @allure.step("Получить счётчик «Выполнено за всё время»")
    def get_completed_all_time(self):
        try:
            return int(self.get_text(OrderLocators.COMPLETED_ALL_TIME))
        except (TimeoutException, ValueError):
            return 0

    @allure.step("Получить счётчик «Выполнено за сегодня»")
    def get_completed_today(self):
        try:
            return int(self.get_text(OrderLocators.COMPLETED_TODAY))
        except (TimeoutException, ValueError):
            return 0

    @allure.step("Дождаться увеличения счётчика «Выполнено за сегодня»")
    def wait_for_completed_today_update(self, initial_value, timeout=15):
        try:
            def _today_updated(driver):
                return self.get_completed_today() > initial_value
            self.wait_for_condition(_today_updated, timeout)
        except TimeoutException:
            pass
        return self.get_completed_today()

    @allure.step("Дождаться исчезновения заглушки «Все заказы готовы»")
    def wait_for_orders_in_progress_ready(self):
        self.wait_for_orders_in_progress(OrderLocators.ALL_ORDERS_READY_TEXT)

    @allure.step("Получить номера заказов в разделе «В работе»")
    def get_orders_in_progress_texts(self):
        try:
            elements = self.find_elements(OrderLocators.ORDERS_IN_PROGRESS)
            return [el.text.strip() for el in elements]
        except TimeoutException:
            return []
