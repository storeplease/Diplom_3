import allure
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.order_page import OrderPage



class TestOrderFeed:

    @allure.title('Открытие всплывающего окна с деталями заказа')
    @allure.description('Проверка, что при клике на заказ в ленте открывается окно с деталями')
    @allure.feature('Лента заказов')
    def test_order_details_modal(self, driver):
        main_page = MainPage(driver)
        order_page = OrderPage(driver)

        main_page.click_order_feed()
        order_page.wait_for_order_feed()

        order_page.click_order_feed_item(index=0)

        assert order_page.is_order_details_visible(), (
            "Всплывающее окно с деталями заказа не появилось"
        )

    @allure.title('Отображение заказов пользователя в ленте заказов')
    @allure.description('Проверка, что заказы из истории отображаются в ленте заказов')
    @allure.feature('Лента заказов')
    def test_user_orders_in_feed(self, driver, order_flow):
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        order_page = OrderPage(driver)

        order_number = order_flow['order_number']

        main_page.click_personal_account()
        login_page.click_order_history()
        order_page.wait_for_order_history()

        main_page.click_order_feed()
        order_page.wait_for_order_feed()
        feed_items = order_page.get_order_feed_items()

        assert any(order_number in item for item in feed_items), (
            f"Номер заказа {order_number} не найден в ленте заказов"
        )

    @allure.title('Увеличение счётчика «Выполнено за всё время»')
    @allure.description('Проверка, что после создания заказа счётчик "Выполнено за всё время" увеличивается')
    @allure.feature('Лента заказов')
    def test_all_time_counter_increases(self, driver, registered_user):
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        order_page = OrderPage(driver)

        payload, access_token = registered_user
        email = payload['email']
        password = payload['password']

        main_page.click_personal_account()
        login_page.enter_login_email(email)
        login_page.enter_login_password(password)
        login_page.click_login_button()

        main_page.click_order_feed()
        initial_all_time = order_page.get_completed_all_time()

        main_page.click_constructor()
        main_page.add_ingredient_to_order(index=0)
        main_page.add_ingredient_to_order(index=2)
        main_page.add_ingredient_to_order(index=6)
        main_page.click_order_button()
        main_page.close_order_modal()

        main_page.click_order_feed()
        updated_all_time = order_page.get_completed_all_time()

        assert updated_all_time > initial_all_time, (
            f"Счётчик 'Выполнено за всё время' не увеличился: "
            f"было {initial_all_time}, стало {updated_all_time}"
        )

    @allure.title('Увеличение счётчика «Выполнено за сегодня»')
    @allure.description('Проверка, что после создания заказа счётчик "Выполнено за сегодня" увеличивается')
    @allure.feature('Лента заказов')
    def test_today_counter_increases(self, driver, registered_user):
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        order_page = OrderPage(driver)

        payload, access_token = registered_user
        email = payload['email']
        password = payload['password']

        main_page.click_personal_account()
        login_page.enter_login_email(email)
        login_page.enter_login_password(password)
        login_page.click_login_button()

        main_page.click_order_feed()
        initial_today = order_page.get_completed_today()
        order_page.wait_for_orders_in_progress_ready()

        main_page.click_constructor()
        main_page.add_ingredient_to_order(index=0)
        main_page.add_ingredient_to_order(index=2)
        main_page.add_ingredient_to_order(index=6)
        main_page.click_order_button()
        main_page.close_order_modal()

        main_page.click_order_feed()
        updated_today = order_page.wait_for_completed_today_update(initial_today)

        assert updated_today > initial_today, (
            f"Счётчик 'Выполнено за сегодня' не увеличился: "
            f"было {initial_today}, стало {updated_today}"
        )

    @allure.title('После оформления заказа раздел «В работе» обновляется')
    @allure.description('Проверка, что после создания заказа его номер появляется в разделе "В работе"')
    @allure.feature('Лента заказов')
    def test_order_number_in_progress(self, driver, order_flow):
        main_page = MainPage(driver)
        order_page = OrderPage(driver)

        order_number = order_flow['order_number']

        main_page.click_order_feed()
        order_page.wait_for_order_feed()

        in_progress_numbers = order_page.get_orders_in_progress_texts()
        assert any(num.lstrip('0') == order_number for num in in_progress_numbers), (
            f"Номер заказа {order_number} не найден в разделе 'В работе'. Найдено: {in_progress_numbers}"
        )
