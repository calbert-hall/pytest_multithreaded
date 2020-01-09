import os
import pytest

from selenium import webdriver
from applitools.selenium import Eyes, Target, BatchInfo, ClassicRunner
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope='module')
def batch_info():
    yield BatchInfo()


@pytest.fixture(name='driver', scope='function')
def driver_setup():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    yield driver
    # Close the browser.
    driver.quit()


@pytest.fixture(name='runner', scope='module')
def runner_setup():
    runner = ClassicRunner()
    yield runner
    all_test_results = runner.get_all_test_results()
    print(all_test_results)


@pytest.fixture(name='eyes', scope='function')
def eyes_setup(runner, batch_info):
    eyes = Eyes(runner)
    # Initialize the eyes SDK and set your private API key.
    eyes.api_key = os.environ['APPLITOOLS_API_KEY']
    eyes.configure.batch = batch_info
    yield eyes
    # If the test was aborted before eyes.close was called, ends the test as aborted.
    eyes.abort_if_not_closed()


def test_tutorial(eyes, driver):
    # Start the test and set the browser's viewport size to 800x600.
    eyes.open(driver, "Test app", "First test", {'width': 800, 'height': 600})
    # Navigate the browser to the "hello world!" web-site.
    driver.get('https://demo.applitools.com')

    # Visual checkpoint #1.
    eyes.check("Login Window test", Target.window())

    # End the test.
    eyes.close(False)
