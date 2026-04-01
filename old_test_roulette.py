from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class RouletteLocators:
    RADIO_MODE_A = "radio_mode_a"
    RADIO_MODE_B = "radio_mode_b"
    RADIO_MODE_C = "radio_mode_c"
    BTN_SPIN = "btn_spin"
    BTN_ADD = "btn_add_item"
    BTN_DIALOG_RESULT_OK = "btn_dialog_result_confirm"  # Kotlin 업데이트 후 적용 가능

    @staticmethod
    def item_text(index): return f"input_item_text_{index}"


class RouletteTester:
    def __init__(self):
        options = UiAutomator2Options()
        options.platform_name = 'Android'
        options.automation_name = 'uiautomator2'
        options.device_name = 'Google Pixel 10 Pro'
        options.app_package = 'com.torimaru.trionroulette'
        options.app_activity = '.MainActivity'
        options.no_reset = False

        self.driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.wait_long = WebDriverWait(self.driver, 20)
        self.loc = RouletteLocators()

    def select_mode(self, mode_locator):
        """모드를 선택합니다."""
        print(f"👉 모드 선택: {mode_locator}")
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, mode_locator))).click()

    def add_items(self, count):
        """항목 추가 버튼을 count만큼 누릅니다."""
        print(f"👉 항목 추가 버튼 {count}회 클릭")
        btn = self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.loc.BTN_ADD)))
        for _ in range(count):
            btn.click()
            time.sleep(0.3)

    def input_menus(self, menus):
        """메뉴 리스트를 입력합니다."""
        for i, menu in enumerate(menus):
            field_id = self.loc.item_text(i)
            print(f"👉 '{field_id}'에 '{menu}' 입력 중...")

            element = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, field_id)))

            # 안전한 스크롤 (에러 무시)
            try:
                self.driver.execute_script('mobile: scrollGesture', {
                    'elementId': element.id, 'direction': 'down', 'percent': 1.0
                })
                time.sleep(0.5)
            except:
                pass

            element.click()
            time.sleep(0.5)

            try:
                element.clear()
            except:
                for _ in range(10): self.driver.press_keycode(67)

            self.driver.execute_script('mobile: type', {'text': menu})
            time.sleep(0.5)

            try:
                self.driver.hide_keyboard()
            except:
                pass
            time.sleep(0.5)

    def spin_and_check_result(self):
        """룰렛을 돌리고 결과를 확인합니다."""
        print("👉 룰렛 돌리기 (SPIN)")
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.loc.BTN_SPIN))).click()

        print("⏳ 결과 대기 중...")
        # Kotlin에 ID를 부여했다면 아래 코드를 사용 (현재는 XPATH 주석 처리)
        # result_ok = self.wait_long.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//*[@text='확인']")))
        result_ok = self.wait_long.until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.loc.BTN_DIALOG_RESULT_OK)))
        result_ok.click()
        print("✅ 팝업 닫기 성공!")

    def quit(self):
        self.driver.quit()
        print("📱 테스트 종료")


# ---------------------------------------------------------
# 실제 테스트 시나리오 실행부
# ---------------------------------------------------------
if __name__ == "__main__":
    tester = RouletteTester()
    try:
        print("🎬 TC-A-01: 기본 모드 정상 실행 테스트 시작")

        # 블록 조립하듯 함수를 호출하여 시나리오 구성
        tester.select_mode(RouletteLocators.RADIO_MODE_A)
        tester.add_items(1)  # 기본 2개 + 1개 추가 = 3개
        tester.input_menus(["삼겹살", "초밥", "마라탕"])
        tester.spin_and_check_result()

        print("🎉 모든 시나리오 테스트가 완벽하게 성공했습니다!")

    except Exception as e:
        print(f"❌ 에러 발생: {e}")
    finally:
        tester.quit()