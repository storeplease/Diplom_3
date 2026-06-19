import allure
from locators.main_page_locators import MainPageLocators
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By

class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.timeout = 15
        self.wait = WebDriverWait(self.driver, self.timeout)

    @allure.step("Открыть страницу {url}")
    def go_to_url(self, url):
        self.driver.get(url)

    def find_element_with_wait(self, locator):
        self.wait.until(EC.visibility_of_element_located(locator))
        return self.driver.find_element(*locator)

    def find_elements(self, locator):
        self.wait.until(EC.presence_of_all_elements_located(locator))
        return self.driver.find_elements(*locator)

    def click_to_element(self, locator):
        self._dismiss_overlay_if_present()
        element = self.wait_element_until_clickable(locator)
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

    def _dismiss_overlay_if_present(self):
        try:
            self.wait_element_until_invisibility(MainPageLocators.OVERLAY, time=5)
        except TimeoutException:
            pass

    def input_text(self, locator, text):
        element = self.find_element_with_wait(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.find_element_with_wait(locator).text

    def is_displayed(self, locator):
        try:
            return self.find_element_with_wait(locator).is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_element_until_clickable(self, locator, time=15):
        return WebDriverWait(self.driver, time).until(EC.element_to_be_clickable(locator))

    def wait_element_until_visibility(self, locator, time=15):
        return WebDriverWait(self.driver, time).until(EC.visibility_of_element_located(locator))

    def wait_element_until_invisibility(self, locator, time=20):
        WebDriverWait(self.driver, time).until(EC.invisibility_of_element_located(locator))

    def get_current_url(self):
        return self.driver.current_url

    def click_using_js(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Перетащить элемент в цель (Drag & Drop)")
    def drag_and_drop(self, source_element, target_element):
        script = """
            function simulateHTML5DragAndDrop(sourceNode, destinationNode) {
                var dataTransfer = new DataTransfer();
                var dragStartEvent = new DragEvent('dragstart', {
                    bubbles: true,
                    cancelable: true,
                    dataTransfer: dataTransfer
                });
                sourceNode.dispatchEvent(dragStartEvent);

                var dropEvent = new DragEvent('drop', {
                    bubbles: true,
                    cancelable: true,
                    dataTransfer: dataTransfer
                });
                destinationNode.dispatchEvent(dropEvent);

                var dragEndEvent = new DragEvent('dragend', {
                    bubbles: true,
                    cancelable: true,
                    dataTransfer: dataTransfer
                });
                sourceNode.dispatchEvent(dragEndEvent);
            }
            simulateHTML5DragAndDrop(arguments[0], arguments[1]);
        """
        self.driver.execute_script(script, source_element, target_element)

    @allure.step("Закрыть модальное окно")
    def close_modal_with_overlay(self, modal_locator, close_button_locator, overlay_locator):
        close_button = self.wait_element_until_clickable(close_button_locator, time=10)
        try:
            close_button.click()
        except Exception:
            self.click_using_js(close_button)

    @allure.step("Получить номер заказа из модалки (ожидание не 9999)")
    def get_order_number(self, order_number_locator):
        try:
            def _valid_order_number(driver):
                text = driver.find_element(*order_number_locator).text.strip()
                return text.isdigit() and text != '9999'
            WebDriverWait(self.driver, 15).until(_valid_order_number)
            return self.driver.find_element(*order_number_locator).text.strip()
        except (TimeoutException, NoSuchElementException):
            return ''

    @allure.step("Дождаться исчезновения заглушки 'Все заказы готовы'")
    def wait_for_orders_in_progress(self, empty_text_locator):
        try:
            self.wait_element_until_invisibility(empty_text_locator, time=10)
        except TimeoutException:
            pass

    def wait_for_url_contains(self, text, time=15):
        WebDriverWait(self.driver, time).until(EC.url_contains(text))

    def wait_for_url_to_be(self, text, time=15):
        WebDriverWait(self.driver, time).until(EC.url_to_be(text))

    def wait_for_condition(self, condition, time=15):
        WebDriverWait(self.driver, time).until(condition)