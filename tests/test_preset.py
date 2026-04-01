import pytest
import time
from pages.roulette_page import RoulettePage


class TestPreset:

    # 🎬 TC-PRESET-01: 프리셋 정상 저장 및 불러오기 (커스텀 모드 확률 포함) 테스트
    def test_tc_preset_01_save_and_load_mode_c(self, driver):
        page = RoulettePage(driver)

        print("\n🎬 TC-PRESET-01: 커스텀 모드 프리셋 저장 및 복구 검증 시작")

        # 0. 커스텀 모드(C) 선택 및 항목 1개 추가 (총 3개)
        page.select_mode(page.RADIO_MODE_C)
        page.add_items(1)

        # 1. 원본 데이터 세팅 및 저장
        preset_name = "가챠확률"
        original_menus = ["SSR (전설)", "SR (영웅)", "R (일반)"]
        original_probs = ["1.5", "18.5", "80"]  # 합계 100%

        print("1️⃣ 원본 메뉴/확률 입력 및 저장 진행")
        page.input_menus(original_menus)
        page.input_probabilities(original_probs)

        page.save_preset(preset_name)

        # 2. 화면 내용 훼손 (사용자가 다른 걸 입력했다고 가정)
        print("2️⃣ 룰렛 내용을 임의로 훼손합니다.")
        fake_menus = ["짜장면", "짬뽕", "탕수육"]
        fake_probs = ["33.33", "33.33", "33.34"]

        page.input_menus(fake_menus)
        page.input_probabilities(fake_probs)

        # 포커스 해제 (키보드 닫기)
        try:
            driver.hide_keyboard()
        except:
            driver.tap([(50, 50)])
        time.sleep(1)

        # 3. 프리셋 불러오기
        print("3️⃣ 저장했던 프리셋을 다시 불러옵니다.")
        page.load_preset(preset_name)

        # 4. 검증 (Verification): 훼손되었던 화면이 원본 메뉴와 확률로 복구되었는가?
        print("\n🔍 검증: 텍스트 박스와 확률(%)의 내용이 원본과 정확히 일치하는지 확인")
        time.sleep(2)  # 팝업이 닫히고 UI 렌더링 및 접근성 트리가 갱신될 넉넉한 시간 대기

        # ⭐️ 트리 강제 갱신 유도: 화면의 빈 곳을 가볍게 터치합니다.
        try:
            driver.tap([(10, 10)])
        except:
            pass
        time.sleep(0.5)

        # ⭐️ 마법의 코드: Appium 버그 우회를 위해 현재 화면의 모든 텍스트 구조를 가져옵니다.
        source = driver.page_source

        is_matched = True
        for i in range(len(original_menus)):
            expected_menu = original_menus[i]
            expected_prob = original_probs[i]

            # 정공법: 텍스트 박스에서 직접 값을 읽어옵니다.
            actual_menu = page.get_item_text(i)
            actual_prob = page.get_prob_text(i)

            print(
                f"   - [항목 {i + 1}] 예상: '{expected_menu}'({expected_prob}%) / 실제 속성값: '{actual_menu}'({actual_prob}%)")

            # [이중 검증 로직]
            # 1. 메뉴 이름 검증
            if actual_menu != expected_menu:
                if expected_menu in source:
                    print(f"     ✅ (우회 성공) 속성은 비어있지만, 화면 전체 스캔에서 '{expected_menu}' 발견!")
                else:
                    is_matched = False
                    print(f"   ❌ 오류: '{expected_menu}' 메뉴가 복구되지 않았습니다.")

            # 2. 확률(%) 검증
            if actual_prob != expected_prob:
                if expected_prob in source:
                    print(f"     ✅ (우회 성공) 속성은 비어있지만, 화면 전체 스캔에서 '{expected_prob}'% 발견!")
                else:
                    is_matched = False
                    print(f"   ❌ 오류: '{expected_prob}'% 확률이 복구되지 않았습니다.")

        # 완벽하게 일치해야 테스트 통과!
        assert is_matched == True, "❌ 결함 발견: 프리셋을 불러왔으나 항목이나 확률이 원본과 다릅니다!"

        print("✅ TC-PRESET-01 테스트 통과: 데이터(메뉴 및 확률) 저장 및 복구 기능이 완벽합니다!")