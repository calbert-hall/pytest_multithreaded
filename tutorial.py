import os
import pytest
import json
import random

from selenium import webdriver
from applitools.selenium import Eyes, Target, BatchInfo, ClassicRunner
from webdriver_manager.chrome import ChromeDriverManager
from filelock import FileLock

@pytest.fixture(name="my_batch_info", scope="session", autouse=True)
def batch_info(tmp_path_factory, worker_id):
    #If there's only 1 thread, it's called master
    if worker_id == "master":
        my_batch_info = BatchInfo("Pytest Batch")
        yield my_batch_info

    root_tmp_dir = tmp_path_factory.getbasetemp().parent
    my_batch_info = BatchInfo("Pytest Batch")
    fn = root_tmp_dir / "data.json"

    with FileLock(str(fn) + ".lock"):
        if fn.is_file():
            my_batch_info.with_batch_id(int(json.loads(fn.read_text())))
        else:
            batchId = random.randint(0, 999999)
            my_batch_info.with_batch_id(batchId)
            fn.write_text(json.dumps(str(batchId)))
    yield my_batch_info


@pytest.fixture(name="driver", scope="function")
def driver_setup():
    """
    New browser instance per test and quite.
    """
    driver = webdriver.Chrome(ChromeDriverManager().install())
    yield driver
    # Close the browser.
    driver.quit()


@pytest.fixture(name="runner", scope="session")
def runner_setup():
    """
    One test runner for all tests. Print test results in the end of execution.
    """
    print("Runner setup called")
    runner = ClassicRunner()
    yield runner
    all_test_results = runner.get_all_test_results()
    print(all_test_results)


@pytest.fixture(name="eyes", scope="function")
def eyes_setup(runner, my_batch_info):
    """
    Basic Eyes setup. It'll abort test if wasn't closed properly.
    """
    eyes = Eyes(runner)
    # Initialize the eyes SDK and set your private API key.
    eyes.api_key = os.environ["APPLITOOLS_API_KEY"]
    eyes.configure.batch = my_batch_info
    yield eyes
    # If the test was aborted before eyes.close was called, ends the test as aborted.
    eyes.abort_if_not_closed()

@pytest.mark.parametrize(
    "testedUrl, testName",
    [("https://demo.applitools.com", "First test"),("https://demo.applitools.com/index_v2.html", "Second Test")]
)
def test_tutorial(eyes, driver, testedUrl, testName):
    # Start the test and set the browser's viewport size to 800x600.
    eyes.open(driver, "Test app", testName, {"width": 800, "height": 600})
    # Navigate the browser to the "hello world!" web-site.
    driver.get(testedUrl)

    # Visual checkpoint #1.
    eyes.check("Login Window test", Target.window())

    # End the test.
    eyes.close(False)
