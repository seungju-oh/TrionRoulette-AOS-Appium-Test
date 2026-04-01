from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class RoulettePage:
    # ==========================================
    # 1. Locators (화면 요소의 고유 ID 모음)
    # ==========================================
    RADIO_MODE_A = "radio_mode_a"
    RADIO_MODE_B = "radio_mode_b"
    RADIO_MODE_C = "radio_mode_c"
    BTN_ADD = "btn_add_item"
    BTN_DIALOG_RESULT_OK = "btn_dialog_result_confirm"

    @staticmethod
    def item_text(index):
        """텍스트 입력칸의 동적 ID를 생성합니다."""
        return f"input_item_text_{index}"

    @staticmethod
    def item_prob(index):
        """확률 입력칸의 동적 ID를 생성합니다."""
        return f"input_item_prob_{index}"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)       # 기본 10초 대기
        self.wait_long = WebDriverWait(driver, 20)  # 룰렛 회전 등 오래 걸리는 작업용 20초 대기

    # ==========================================
    # 2. 공통 유틸리티 (도우미 함수들)
    # ==========================================
    def hide_keyboard_safe(self):
        """[공통] 안전하게 키보드를 숨기거나 포커스를 해제하여 상태를 동기화합니다."""
        try:
            self.driver.hide_keyboard()
        except:
            # 키보드가 이미 내려가 있다면 화면 중앙 빈 곳을 터치하여 포커스 해제
            self.driver.tap([(50, 50)])
        time.sleep(1) # UI가 안정될 시간 부여

    # ==========================================
    # 3. 주요 액션 (앱 조작 로직)
    # ==========================================
    def select_mode(self, mode_locator):
        """상단의 룰렛 모드(A, B, C) 라디오 버튼을 선택합니다."""
        print(f"\n👉 모드 선택: {mode_locator}")
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, mode_locator))).click()

    def add_items(self, count):
        """'+ 항목 추가' 버튼을 원하는 횟수만큼 클릭합니다."""
        print(f"👉 항목 추가 버튼 {count}회 클릭")
        btn = self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.BTN_ADD)))
        for _ in range(count):
            btn.click()
            time.sleep(0.3)

    def input_menus(self, menus):
        """항목(메뉴) 이름 입력창에 텍스트를 입력합니다."""
        for i, menu in enumerate(menus):
            field_id = self.item_text(i)
            print(f"👉 '{field_id}'에 '{menu}' 입력 중...")

            element = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, field_id)))

            # 화면 아래쪽에 가려져 있을 경우를 대비해 스크롤
            try:
                self.driver.execute_script('mobile: scrollGesture', {'elementId': element.id, 'direction': 'down', 'percent': 1.0})
                time.sleep(0.5)
            except: pass

            element.click()
            time.sleep(0.5)

            # 기존 텍스트 물리적 삭제 (Appium clear 무시 버그 우회)
            self.driver.press_keycode(123)  # 커서를 맨 뒤로
            for _ in range(20): self.driver.press_keycode(67)  # 백스페이스 연타

            # 새 텍스트 입력
            self.driver.execute_script('mobile: type', {'text': menu})
            time.sleep(0.5)

            self.hide_keyboard_safe()

    def input_probabilities(self, probabilities):
        """커스텀 모드(C)의 확률(%) 입력창에 값을 입력합니다."""
        for i, prob in enumerate(probabilities):
            field_id = self.item_prob(i)
            print(f"👉 '{field_id}'에 확률 '{prob}%' 입력 중...")

            element = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, field_id)))

            try:
                self.driver.execute_script('mobile: scrollGesture', {'elementId': element.id, 'direction': 'down', 'percent': 1.0})
                time.sleep(0.5)
            except: pass

            element.click()
            time.sleep(0.5)

            # 기존 확률 물리적 삭제
            self.driver.press_keycode(123)
            for _ in range(10): self.driver.press_keycode(67)

            # 새 확률 입력
            self.driver.execute_script('mobile: type', {'text': str(prob)})
            time.sleep(0.5)

            self.hide_keyboard_safe()

    def delete_item(self, index):
        """특정 인덱스의 항목 삭제(휴지통) 버튼을 클릭합니다."""
        btn_id = f"btn_delete_item_{index}"
        print(f"👉 '{btn_id}' (항목 {index + 1} 삭제) 클릭 시도...")

        element = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, btn_id)))
        try:
            self.driver.execute_script('mobile: scrollGesture', {'elementId': element.id, 'direction': 'down', 'percent': 1.0})
            time.sleep(0.5)
        except: pass

        element.click()
        time.sleep(1)

    def spin_roulette(self):
        """START SPIN 버튼을 클릭하여 룰렛을 회전시킵니다."""
        print("👉 'START SPIN' 버튼 클릭 (룰렛 회전)")
        # 'btn_spin_enabled'라는 동적 ID를 직접 찾아 누릅니다.
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "btn_spin_enabled"))).click()

    # ==========================================
    # 4. 검증 및 상태 확인 (상태 읽어오기)
    # ==========================================
    def is_spin_button_enabled(self):
        """스핀 버튼이 활성화되어 있는지 동적 ID로 판단합니다."""
        time.sleep(1)
        try:
            self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "btn_spin_enabled")
            print("   👉 [Appium 인식] 활성화 상태입니다!")
            return True
        except: pass

        try:
            self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "btn_spin_disabled")
            print("   👉 [Appium 인식] 비활성화(잠김) 상태입니다!")
            return False
        except:
            return False

    def check_item_enabled(self, index):
        """항목 텍스트 박스가 활성화되어 있는지(서바이벌 제외 여부) 동적 ID로 판단합니다."""
        time.sleep(1)
        normal_id = f"input_item_text_{index}"
        disabled_id = f"input_item_text_{index}_disabled"

        try:
            self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, disabled_id)
            print(f"   👉 [Appium 인식] 잠김(제외) 상태입니다!")
            return False
        except: pass

        try:
            self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, normal_id)
            print(f"   👉 [Appium 인식] 활성화 상태입니다!")
            return True
        except:
            return False

    def get_item_count(self):
        """현재 화면에 생성된 항목 텍스트 박스의 총 개수를 세어 반환합니다."""
        elements = self.driver.find_elements(AppiumBy.XPATH, "//*[contains(@content-desc, 'input_item_text_')]")
        return len(elements)

    def get_item_text(self, index):
        """텍스트 박스의 현재 입력값을 강제로 읽어옵니다."""
        field_id = self.item_text(index)
        element = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, field_id)))
        val = element.get_attribute("text")
        return val if val is not None else ""

    def get_prob_text(self, index):
        """확률 박스의 현재 입력값을 강제로 읽어옵니다."""
        time.sleep(1.5)
        field_id = self.item_prob(index)
        element = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, field_id)))
        val = element.get_attribute("text")
        return val if val is not None else ""

    # ==========================================
    # 5. 팝업 제어 (결과창, 덮어쓰기 창 등)
    # ==========================================
    def check_result_popup(self):
        """단순히 팝업이 뜰 때까지 기다렸다가 '확인'을 눌러 닫습니다."""
        print("⏳ 결과 팝업 대기 후 닫기...")
        result_ok = self.wait_long.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.BTN_DIALOG_RESULT_OK)))
        result_ok.click()
        return True

    def get_result_and_close_popup(self):
        """당첨 팝업에서 텍스트(예: 피자 당첨!)를 추출한 뒤 닫습니다."""
        print("⏳ 당첨 결과 추출 대기 중...")
        result_text_element = self.wait_long.until(EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@text, '당첨')]")))
        raw_text = result_text_element.text
        print(f"🎉 팝업 텍스트: '{raw_text}'")

        result_ok = self.wait_long.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.BTN_DIALOG_RESULT_OK)))
        result_ok.click()
        return raw_text

    def is_popup_present(self, timeout=3):
        """[신규] 지정된 시간 동안 팝업이 뜨는지 여부를 반환합니다. (중복 클릭 방어 테스트용)"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, self.BTN_DIALOG_RESULT_OK))
            )
            return True
        except TimeoutException:
            return False

    # ==========================================
    # 6. 프리셋 저장 / 불러오기
    # ==========================================
    def save_preset(self, preset_name):
        """현재 상태를 프리셋으로 저장하며, 중복 시 덮어쓰기 팝업도 자동 처리합니다."""
        print(f"\n👉 프리셋 '{preset_name}' 저장 중...")
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "btn_topbar_save"))).click()

        input_field = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "input_preset_name")))
        input_field.click()
        time.sleep(0.5)

        self.driver.press_keycode(123)
        for _ in range(15): self.driver.press_keycode(67)

        self.driver.execute_script('mobile: type', {'text': preset_name})
        time.sleep(0.5)
        self.hide_keyboard_safe()

        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "btn_dialog_save_confirm"))).click()

        try:
            short_wait = WebDriverWait(self.driver, 1.5)
            overwrite_btn = short_wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "btn_dialog_overwrite_confirm")))
            print("   ⚠️ 기존 데이터 '덮어쓰기' 승인")
            overwrite_btn.click()
        except TimeoutException:
            print("   ✅ 최초 저장 완료 (덮어쓰기 없음)")
            pass

        time.sleep(1)

    def load_preset(self, preset_name):
        """저장된 프리셋 목록에서 선택하여 불러옵니다."""
        print(f"\n👉 프리셋 '{preset_name}' 불러오는 중...")
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "btn_topbar_load"))).click()
        time.sleep(0.5)

        preset_row_id = f"row_load_preset_{preset_name}"
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, preset_row_id))).click()
        time.sleep(1)