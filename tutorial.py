from selenium import webdriver
from applitools.selenium import Eyes, Target
import os


class HelloWorld:

    eyes = Eyes()

    # Initialize the eyes SDK and set your private API key.
    eyes.api_key = os.environ['APPLITOOLS_API_KEY']

    try:

        # Open a Chrome browser.
        driver = webdriver.Chrome()

        # Start the test and set the browser's viewport size to 800x600.
        eyes.open(driver, "Test app", "First test", {'width': 800, 'height': 600})

        # Navigate the browser to the "hello world!" web-site.
        driver.get('https://demo.applitools.com')

        # Visual checkpoint #1.
        eyes.check("Login Window test", Target.window())

        # End the test.
        eyes.close()

    finally:

        # Close the browser.
        driver.quit()

        # If the test was aborted before eyes.close was called, ends the test as aborted.
        eyes.abort()