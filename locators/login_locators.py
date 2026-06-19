from selenium.webdriver.common.by import By


class LoginLocators:
    LOGIN_EMAIL_INPUT = By.XPATH, ".//label[text()='Email']/following-sibling::input"
    LOGIN_PASSWORD_INPUT = By.XPATH, ".//label[text()='Пароль']/following-sibling::input"
    LOGIN_BUTTON = By.XPATH, "//button[text()='Войти']"
    RESTORE_PASSWORD_LINK = By.XPATH, "//a[text()='Восстановить пароль']"

    RESTORE_EMAIL_INPUT = By.XPATH, "//input[@name='name']"
    RESTORE_BUTTON = By.XPATH, "//button[text()='Восстановить']"

    PASSWORD_FIELD_PASSIVE = By.XPATH, "//div[contains(@class, 'input_type_password')]//input"
    PASSWORD_FIELD_ACTIVE = By.XPATH, "//div[contains(@class, 'input_type_text')]//input"
    TOGGLE_PASSWORD_VISIBILITY = By.XPATH, "//div[contains(@class, 'input__icon-action')]"

    LOGOUT_BUTTON = By.XPATH, "//button[contains(., 'Выход')]"

    ORDER_HISTORY_LINK = By.XPATH, "//a[@href='/account/order-history']"
