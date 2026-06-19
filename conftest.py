import pytest
import allure
import requests
from selenium import webdriver
from urls import BASE_URL, API_BASE_URL
from data import ENDPOINTS
from helpers import Helpers
from pages.main_page import MainPage
from pages.login_page import LoginPage


@pytest.fixture(params=['Chrome', 'Firefox'])
def driver(request):
    browser = request.param
    if browser == 'Chrome':
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--headless")
        web_driver = webdriver.Chrome(options=options)
    elif browser == 'Firefox':
        options = webdriver.FirefoxOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--headless")
        web_driver = webdriver.Firefox(options=options)
    web_driver.get(BASE_URL)
    yield web_driver
    web_driver.quit()


@allure.step("Регистрация нового пользователя через API")
def register_user():
    helper = Helpers()
    payload = {
        'email': helper.generate_email(),
        'password': helper.generate_password(),
        'name': f'User{helper.generate_random_string(5)}'
    }
    response = requests.post(
        f'{API_BASE_URL}{ENDPOINTS["register"]}',
        json=payload,
        timeout=10
    )
    return payload, response


@allure.step("Удаление пользователя через API")
def delete_user(access_token):
    headers = {'Authorization': access_token}
    requests.delete(
        f'{API_BASE_URL}{ENDPOINTS["user"]}',
        headers=headers,
        timeout=10
    )


@pytest.fixture
def registered_user():
    payload, response = register_user()
    user_data = response.json()
    access_token = user_data.get('accessToken')
    yield payload, access_token
    if access_token:
        delete_user(access_token)


@pytest.fixture(params=[(0, 2, 6), (1, 3, 7)])
def order_flow(driver, registered_user, request):
    main_page = MainPage(driver)
    login_page = LoginPage(driver)

    payload, access_token = registered_user
    email = payload['email']
    password = payload['password']

    main_page.click_personal_account()
    login_page.enter_login_email(email)
    login_page.enter_login_password(password)
    login_page.click_login_button()

    for idx in request.param:
        main_page.add_ingredient_to_order(index=idx)

    main_page.click_order_button()
    order_number = main_page.get_order_number_from_modal()
    main_page.close_order_modal()

    return {'order_number': order_number}
