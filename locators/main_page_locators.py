from selenium.webdriver.common.by import By


class MainPageLocators:
    CONSTRUCTOR_BUTTON = By.XPATH, "//p[text()='Конструктор']/parent::a"
    ORDER_FEED_LINK = By.XPATH, "//p[text()='Лента Заказов']/parent::a"
    PERSONAL_ACCOUNT_BUTTON = By.XPATH, "//a[contains(@class, 'AppHeader_header__link') and contains(., 'Личный Кабинет')]"

    INGREDIENT = By.XPATH, "//a[contains(@class, 'BurgerIngredient_ingredient')]"

    TARGET_AREA = By.XPATH, "//ul[contains(@class, 'BurgerConstructor_basket__list')]"

    MODAL_WINDOW = By.XPATH, "//section[contains(@class, 'Modal_modal_opened')]//div[contains(@class, 'Modal_modal__container')]"
    CLOSE_MODAL_BUTTON = By.XPATH, "//section[contains(@class, 'Modal_modal_opened')]//button[contains(@class, 'Modal_modal__close')]"
    MODAL_OVERLAY = By.XPATH, "//section[contains(@class, 'Modal_modal_opened')]/div[contains(@class, 'Modal_modal_overlay')]"

    INGREDIENT_COUNTER = By.XPATH, "//a[contains(@class, 'BurgerIngredient_ingredient')]//p[contains(@class, 'counter__num')]"

    ORDER_BUTTON = By.XPATH, "//button[text()='Оформить заказ']"

    ORDER_MODAL_CONTAINER = By.XPATH, "//section[contains(@class, 'Modal_modal_opened')]//div[contains(@class, 'Modal_modal__container')]"
    ORDER_NUMBER = By.XPATH, "//section[contains(@class, 'Modal_modal_opened')]//h2[contains(@class, 'Modal_modal__title') and contains(@class, 'text_type_digits-large')]"
    CLOSE_ORDER_MODAL_BUTTON = By.XPATH, "//section[contains(@class, 'Modal_modal_opened')]//button[contains(@class, 'Modal_modal__close')]"
