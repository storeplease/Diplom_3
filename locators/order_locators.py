from selenium.webdriver.common.by import By


class OrderLocators:
    ORDER_FEED_LIST = By.XPATH, "//ul[contains(@class, 'OrderFeed_orderList')]"
    ORDER_FEED_ITEM = By.XPATH, "//li[contains(@class, 'OrderHistory_listItem')]"

    ORDER_DETAILS_MODAL = By.XPATH, "//section[contains(@class, 'Modal_modal_opened')]"

    ORDER_HISTORY_LIST = By.XPATH, "//ul[contains(@class, 'OrderHistory_profileList')]"

    COMPLETED_ALL_TIME = By.XPATH, "//p[text()='Выполнено за все время:']/following-sibling::p[contains(@class, 'OrderFeed_number')]"
    COMPLETED_TODAY = By.XPATH, "//p[text()='Выполнено за сегодня:']/following-sibling::p[contains(@class, 'OrderFeed_number')]"

    ORDERS_IN_PROGRESS = By.XPATH, "//ul[contains(@class, 'OrderFeed_orderListReady')]/li[contains(@class, 'text_type_digits-default')]"
    ALL_ORDERS_READY_TEXT = By.XPATH, "//li[text()='Все текущие заказы готовы!']"
