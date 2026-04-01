import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options


# @pytest.fixture는 테스트가 시작될 때마다 자동으로 실행되는 준비/마무리 작업입니다.
@pytest.fixture(scope="function")
def driver():
    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.automation_name = 'uiautomator2'
    options.device_name = 'Google Pixel 10 Pro'
    options.app_package = 'com.torimaru.trionroulette'
    options.app_activity = '.MainActivity'
    options.no_reset = False  # 매 테스트마다 앱을 초기화하려면 False

    # 1. 앱 실행 (Setup)
    driver = webdriver.Remote('http://127.0.0.1:4723', options=options)

    # 2. 테스트 함수로 드라이버 전달
    yield driver

    # 3. 테스트 종료 후 앱 닫기 (Teardown)
    driver.quit()