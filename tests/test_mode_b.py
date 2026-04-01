import pytest
import time
from pages.roulette_page import RoulettePage


class TestModeB:

    # 🎬 TC-B-01: 서바이벌 모드 당첨 항목 제외(비활성화) 테스트
    def test_tc_b_01_survival_exclusion(self, driver):
        page = RoulettePage(driver)

        print("\n🎬 TC-B-01: 서바이벌 모드 제외 처리 테스트 시작")

        # 1. 서바이벌 모드(B) 선택
        page.select_mode(page.RADIO_MODE_B)

        # 2. 항목 세팅 (총 3개)
        menus = ["피자", "치킨", "햄버거"]
        page.add_items(1)
        page.input_menus(menus)

        # 3. 룰렛 돌리기
        page.spin_roulette()

        # 4. 팝업 원본 텍스트 가져오기 (예: "피자 당첨!")
        raw_winner_text = page.get_result_and_close_popup()

        # 5. 부분 일치 검색 (안전한 방식 ⭐)
        winner_menu = None
        winner_index = -1

        for i, menu in enumerate(menus):
            if menu in raw_winner_text:  # "피자 당첨!" 안에 "피자"가 포함되어 있다면
                winner_menu = menu
                winner_index = i
                break

        # 만약 글자를 못 찾았다면 여기서 에러를 내서 알려줌
        assert winner_index != -1, f"❌ 에러: 팝업 텍스트('{raw_winner_text}') 안에서 입력한 메뉴를 찾을 수 없습니다."

        # 6. 검증 (Verification): 찾은 항목의 입력칸이 잠겼는지(disabled) 확인
        is_enabled = page.check_item_enabled(winner_index)

        print(f"🔍 검증: '{winner_menu}' 항목의 활성화 상태는? -> {is_enabled}")

        # is_enabled가 False여야 비활성화(제외)된 것이므로 테스트 통과
        assert is_enabled == False, f"❌ 결함 발견: 당첨된 '{winner_menu}' 항목이 비활성화(제외)되지 않았습니다!"

        print("✅ TC-B-01 테스트 통과: 서바이벌 모드 제외 로직이 정상 작동합니다.")

    # 🎬 TC-B-02: 서바이벌 모드 모든 항목 소진 시 자동 초기화 테스트
    def test_tc_b_02_survival_auto_reset(self, driver):
        page = RoulettePage(driver)

        print("\n🎬 TC-B-02: 모든 항목 소진 시 자동 초기화 테스트 시작")

        # 1. 서바이벌 모드(B) 선택 및 항목 세팅 (총 3개)
        page.select_mode(page.RADIO_MODE_B)
        menus = ["짜장면", "짬뽕", "탕수육"]
        page.add_items(1)
        page.input_menus(menus)

        # 2. 항목 개수(3개)만큼 룰렛을 반복해서 돌립니다.
        # 모드 B는 당첨된 항목이 제외되므로, 3번 돌리면 모든 항목이 정확히 1번씩 당첨됩니다.
        for i in range(3):
            print(f"\n🔄 {i + 1}번째 룰렛 스핀 실행...")
            page.spin_roulette()

            raw_winner_text = page.get_result_and_close_popup()
            print(f"   -> 팝업 확인 완료: '{raw_winner_text}'")
            time.sleep(1)  # UI가 제외 처리될 시간을 살짝 줍니다.

        # ==========================================================
        # 3. 마지막 3번째 팝업이 닫힌 직후, 초기화 로직 검증 (Verification)
        print("\n🔍 검증: 모든 항목이 소진되어 전체 초기화(부활)가 되었는지 확인")
        time.sleep(2)  # 팝업이 닫히고 UI가 초기화될 시간을 줍니다.

        all_enabled = True
        for i, menu in enumerate(menus):
            # 상태 검사
            is_enabled = page.check_item_enabled(i)
            print(f"   - '{menu}' (항목 {i + 1}) 활성화 상태: {is_enabled}")

            if is_enabled == False:
                all_enabled = False
                print(f"   ❌ 오류: '{menu}' 항목이 아직 비활성화 상태입니다.")

        # 모든 항목이 True(활성화) 상태여야 테스트 통과!
        assert all_enabled == True, "❌ 결함 발견: 모든 항목이 소진되었으나 초기화(부활)되지 않았습니다!"

        print("✅ TC-B-02 테스트 통과: 자동 초기화 로직이 완벽하게 작동합니다!")