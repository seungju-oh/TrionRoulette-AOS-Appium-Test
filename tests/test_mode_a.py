import pytest
import time
from pages.roulette_page import RoulettePage


class TestModeA:

    # 🎬 TC-COM-E03: 최소 항목(2개) 미만 삭제 방어 로직 검증
    def test_tc_com_e03_min_items_defense(self, driver):
        page = RoulettePage(driver)
        print("\n🎬 TC-COM-E03: 최소 항목(2개) 삭제 방어 로직 검증 시작")

        print("1️⃣ 항목 2개에 정상적인 이름 입력")
        page.input_menus(["짜장면", "짬뽕"])
        # (input_menus 함수 안에 hide_keyboard_safe가 포함되어 있어 코드가 훨씬 짧아졌습니다)

        print("2️⃣ 항목이 2개인 상태에서 삭제 버튼 터치 시도")
        page.delete_item(0)

        print("\n🔍 검증: 방어 로직에 의해 항목 개수가 2개로 유지되는지 확인")
        after_delete_count = page.get_item_count()
        assert after_delete_count == 2, f"❌ 결함 발견: 항목이 2개일 때 삭제가 수행되었습니다! (현재: {after_delete_count}개)"

        is_spin_enabled = page.is_spin_button_enabled()
        assert is_spin_enabled == True, "❌ 결함 발견: 이름이 모두 입력된 2개 항목인데 스핀 버튼이 비활성화되었습니다."

        print("✅ TC-COM-E03 통과: 최소 항목 2개 삭제 방어 로직 완벽 작동!")

    # 🎬 TC-COM-E04: 빈 텍스트 입력 시 스핀 버튼 방어 로직 검증
    def test_tc_com_e04_empty_text_defense(self, driver):
        page = RoulettePage(driver)
        print("\n🎬 TC-COM-E04: 빈 텍스트 입력 시 스핀 버튼 방어 검증 시작")

        print("1️⃣ 첫 번째 항목의 텍스트를 지워서 빈 칸으로 만듦")
        page.input_menus(["", "짬뽕"])

        print("\n🔍 검증: 항목 이름이 하나라도 비어있을 때 스핀 버튼이 잠기는지 확인")
        is_spin_enabled = page.is_spin_button_enabled()
        assert is_spin_enabled == False, "❌ 결함 발견: 빈 텍스트가 있는데 스핀 버튼이 활성화되어 있습니다!"

        print("✅ TC-COM-E04 통과: 빈 텍스트 입력 시 스핀 방어 로직 완벽 작동!")

    # 🎬 TC-A-01: 기본 모드 정상 실행 테스트
    def test_tc_a_01_normal_spin(self, driver):
        page = RoulettePage(driver)
        page.select_mode(page.RADIO_MODE_A)
        page.add_items(1)
        page.input_menus(["삼겹살", "초밥", "마라탕"])

        page.spin_roulette()
        is_popup_closed = page.check_result_popup()
        assert is_popup_closed == True

    # 🎬 TC-A-E01: 스핀 중복 실행(따닥) 방어 테스트
    def test_tc_a_e01_prevent_double_spin(self, driver):
        page = RoulettePage(driver)
        page.select_mode(page.RADIO_MODE_A)
        page.add_items(1)
        page.input_menus(["짜장면", "짬뽕", "탕수육"])

        # 사용자가 악의적으로 버튼을 아주 빠르게 3번 누름
        for _ in range(3):
            page.spin_roulette()

        # 첫 번째 정상 팝업 닫기
        page.check_result_popup()

        # 중복 팝업(2번째 팝업)이 뜨는지 3초간 확인 (새로 만든 is_popup_present 활용)
        print("🔍 검증: 중복 클릭 방어(2번째 팝업 미발생) 확인 중...")
        is_duplicate_popup_shown = page.is_popup_present(timeout=3)

        # 팝업이 나타나지 않아야(False) 방어 성공
        assert is_duplicate_popup_shown == False, "❌ 결함: 중복 클릭 방어 실패, 팝업이 2개 이상 떴습니다."
        print("✅ TC-A-E01 통과: 스핀 중복 클릭 방어가 완벽하게 동작합니다!")