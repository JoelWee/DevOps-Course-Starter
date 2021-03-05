from threading import Thread

import app
import pytest
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True


@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox(options=options) as driver:
        yield driver


@pytest.fixture(scope="module")
def test_app():
    application = app.create_app()
    application.config["LOGIN_DISABLED"] = True

    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application
    # Tear Down
    thread.join(1)
    mongo_client = MongoClient(application.config["MONGO_URI"])
    mongo_client.drop_database(mongo_client.get_default_database().name)


def test_task_journey(driver, test_app):
    driver.get("http://localhost:5000/")
    assert driver.title == "To-Do App"


def test_item_workflow(driver, test_app):
    driver.get("http://localhost:5000/")
    item_name = "test"

    driver.implicitly_wait(10)  # seconds

    # Create item
    elem = driver.find_element_by_name("title")
    assert elem
    elem.send_keys(item_name)
    elem.send_keys(Keys.RETURN)

    elem = driver.find_element_by_xpath(f"//form[@id='do-{item_name}']/button")
    assert elem

    # Do item
    elem.send_keys(Keys.RETURN)
    elem = driver.find_element_by_xpath(f"//form[@id='complete-{item_name}']/button")
    assert elem

    # Complete item
    elem.send_keys(Keys.RETURN)
    elem = driver.find_element_by_xpath(f"//form[@id='reset-{item_name}']/button")
    assert elem

    # Reset item
    elem.send_keys(Keys.RETURN)
    elem = driver.find_element_by_xpath(f"//form[@id='do-{item_name}']/button")
    assert elem
