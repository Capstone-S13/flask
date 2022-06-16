# from selenium import webdriver
# from selenium.webdriver.common.by import By


# def test_eight_components():
#     driver = webdriver.Safari()

#     driver.get("https://google.com")

#     title = driver.title
#     assert title == "Google"

#     driver.implicitly_wait(0.5)

#     search_box = driver.find_element(by=By.NAME, value="q")
#     search_button = driver.find_element(by=By.NAME, value="btnK")

#     search_box.send_keys("Selenium")
#     search_button.click()

#     search_box = driver.find_element(by=By.NAME, value="q")
#     value = search_box.get_attribute("value")
#     assert value == "Selenium"

#     driver.quit()


import pytest
from application import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()