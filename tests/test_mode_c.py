import pytest
import time
from pages.roulette_page import RoulettePage

class TestModeC:

    def test_tc_c_01_custom_probability(self, driver):
        page = RoulettePage(driver)
        print("\n🎬 TC-C-01: 커스텀 모드 확률 적용 테스트 시작")

        page.select_mode(page.RADIO_MODE_C)
        menus = ["SSR (전설)", "SR (영웅)", "R (일반)"]
        probs = ["1", "19", "80"]

        page.add_items(1)
        page.input_menus(menus)
        page.input_probabilities(probs)

        page.spin_roulette()
        raw_winner_text = page.get_result_and_close_popup()

        winner_menu = None
        for menu in menus:
            if menu in raw_winner_text:
                winner_menu = menu
                break

        print(f"🔍 당첨 결과 분석: '{winner_menu}' 당첨! (설정 확률: SSR 1%, SR 19%, R 80%)")
        assert winner_menu is not None, f"❌ 결함 발견: 이상한 결과('{raw_winner_text}')가 나왔습니다!"
        print("✅ TC-C-01 테스트 통과: 커스텀 확률 모드가 정상적으로 작동합니다.")

    def test_tc_c_02_prob_format_limit(self, driver):
        page = RoulettePage(driver)
        print("\n🎬 TC-C-02: 확률 입력 형식 제한(n.nn%) 검증 시작")

        page.select_mode(page.RADIO_MODE_C)
        invalid_prob = "12.345"
        expected_prob = "12.34"

        print(f"👉 확률창에 '{invalid_prob}' 입력을 시도합니다.")
        page.input_probabilities([invalid_prob])
        # (input_probabilities 내부에 hide_keyboard_safe가 있어 대기만 하면 됨)
        time.sleep(1)

        print(f"🔍 검증: 화면 내에 '{expected_prob}'가 존재하고 '{invalid_prob}'는 방어되었는지 확인")
        source = driver.page_source

        if invalid_prob in source:
            assert False, f"❌ 결함 발견: 소수점 셋째 자리({invalid_prob})가 입력되었습니다!"

        assert expected_prob in source, f"❌ 결함 발견: 기대하는 값({expected_prob})을 화면에서 찾을 수 없습니다."
        print("✅ TC-C-02 테스트 통과: 소수점 둘째 자리까지만 입력되도록 완벽히 제한됨!")

    def test_tc_c_e01_prob_sum_validation(self, driver):
        page = RoulettePage(driver)
        print("\n🎬 TC-C-E01: 확률 합산 오류(99.99% / 100.01%) 스핀 방어 검증")

        page.select_mode(page.RADIO_MODE_C)
        page.add_items(1)

        # 1. 99.99% 상황 테스트
        page.input_probabilities(["33.33", "33.33", "33.33"])
        is_enabled_99 = page.is_spin_button_enabled()
        assert is_enabled_99 == False, "❌ 결함: 총합이 99.99%인데 스핀 버튼이 활성화되었습니다!"

        # 2. 100.01% 상황 테스트
        page.input_probabilities(["33.34", "33.34", "33.33"])
        is_enabled_100_01 = page.is_spin_button_enabled()
        assert is_enabled_100_01 == False, "❌ 결함: 총합이 100.01%인데 스핀 버튼이 활성화되었습니다!"

        print("✅ TC-C-E01 통과: 총합이 100.00%가 아닐 때 스핀 버튼이 정상적으로 차단됩니다.")

    def test_tc_c_e02_zero_percent_prob(self, driver):
        page = RoulettePage(driver)
        print("\n🎬 TC-C-E02: 0% 확률 당첨 제외 로직 검증")

        page.select_mode(page.RADIO_MODE_C)
        page.add_items(1)
        page.input_menus(["확률100", "확률0_A", "확률0_B"])
        page.input_probabilities(["100", "0", "0"])

        page.spin_roulette()
        winner = page.get_result_and_close_popup()

        assert "확률100" in winner, f"❌ 결함: 0% 확률 항목이 당첨되는 치명적 오류 발생! (결과: {winner})"
        print("✅ TC-C-E02 통과: 0% 확률 항목은 룰렛 결과에서 완벽히 제외됩니다.")

    def test_tc_c_e03_invalid_string_input(self, driver):
        page = RoulettePage(driver)
        print("\n🎬 TC-C-E03: 확률 필드 특수문자 입력 방어 검증")

        page.select_mode(page.RADIO_MODE_C)
        invalid_text = "!@#$"
        page.input_probabilities([invalid_text])

        source = driver.page_source
        assert invalid_text not in source, "❌ 결함: 특수문자가 확률 입력창에 그대로 입력되었습니다!"
        print("✅ TC-C-E03 통과: 특수문자 등 비정상 입력이 완벽하게 방어(마스킹)됩니다.")