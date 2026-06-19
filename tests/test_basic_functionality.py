import allure
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.order_page import OrderPage



class TestBasicFunctionality:

    @allure.title('Переход по клику на «Конструктор»')
    @allure.description('Проверка, что клик по кнопке "Конструктор" возвращает на главную страницу')
    @allure.feature('Основной функционал')
    def test_click_to_constructor(self, driver):
        main_page = MainPage(driver)

        main_page.click_order_feed()
        main_page.click_constructor()

        assert main_page.is_constructor_displayed(), (
            "Конструктор не отображается после клика"
        )

    @allure.title('Переход по клику на «Лента заказов»')
    @allure.description('Проверка перехода на страницу ленты заказов по клику на кнопку')
    @allure.feature('Основной функционал')
    def test_click_to_order_feed(self, driver):
        main_page = MainPage(driver)
        order_page = OrderPage(driver)

        main_page.click_order_feed()

        assert order_page.is_feed_displayed(), (
            "Лента заказов не отображается после клика"
        )

    @allure.title('Появление всплывающего окна с деталями ингредиента')
    @allure.description('Проверка, что при клике на ингредиент открывается модальное окно с его деталями')
    @allure.feature('Основной функционал')
    def test_ingredient_modal_appears(self, driver):
        main_page = MainPage(driver)

        main_page.click_ingredient(index=0)

        assert main_page.is_ingredient_modal_visible(), (
            "Модальное окно с деталями ингредиента не появилось"
        )

    @allure.title('Закрытие всплывающего окна кликом по крестику')
    @allure.description('Проверка, что модальное окно закрывается при клике на крестик')
    @allure.feature('Основной функционал')
    def test_close_ingredient_modal(self, driver):
        main_page = MainPage(driver)

        main_page.click_ingredient(index=0)
        main_page.close_ingredient_modal()

        assert main_page.is_ingredient_modal_closed(), (
            "Модальное окно с деталями ингредиента не закрылось"
        )

    @allure.title('Увеличение каунтера ингредиента при добавлении в заказ')
    @allure.description('Проверка, что после добавления ингредиента счётчик увеличивается')
    @allure.feature('Основной функционал')
    def test_ingredient_counter_increases(self, driver):
        main_page = MainPage(driver)

        initial_count = main_page.get_ingredient_counter(index=0)
        main_page.add_ingredient_to_order(index=0)
        main_page.wait_for_counter_change(index=0, initial_value=initial_count)
        main_page.add_ingredient_to_order(index=2)
        main_page.add_ingredient_to_order(index=6)

        updated_count = main_page.get_ingredient_counter(index=0)
        assert updated_count > initial_count, (
            f"Каунтер не увеличился: было {initial_count}, стало {updated_count}"
        )

    @allure.title('Оформление заказа авторизованным пользователем')
    @allure.description('Проверка, что залогиненный пользователь может оформить заказ')
    @allure.feature('Основной функционал')
    def test_logged_user_can_place_order(self, driver, registered_user):
        main_page = MainPage(driver)
        login_page = LoginPage(driver)

        payload, access_token = registered_user
        email = payload['email']
        password = payload['password']

        main_page.click_personal_account()
        login_page.enter_login_email(email)
        login_page.enter_login_password(password)
        login_page.click_login_button()

        main_page.add_ingredient_to_order(index=0)
        main_page.add_ingredient_to_order(index=2)
        main_page.add_ingredient_to_order(index=6)
        main_page.click_order_button()

        assert main_page.is_order_modal_visible(), (
            "Модальное окно с подтверждением заказа не появилось"
        )
