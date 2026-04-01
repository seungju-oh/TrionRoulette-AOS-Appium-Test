# Android Roulette App - QA UI Automation Test

Appium으로 자동화를 구축하기 위해 AI를 사용하여 AOS/iOS 앱을 만든 뒤 AI를 사용하여 구축 한 프로젝트입니다.
Jetpack Compose로 개발된 안드로이드 룰렛 앱의 핵심 기능과 예외 상황(Edge Cases)을 검증하기 위한 **Appium UI 자동화 테스트 프로젝트**입니다. 
유지보수성과 확장성을 고려하여 **POM (Page Object Model)** 디자인 패턴을 적용했습니다.

## Tech Stack
- **Language:** Python 3.x
- **Testing Framework:** Pytest
- **Automation Tool:** Appium, Selenium WebDriver
- **Target OS:** Android

## Project Architecture (POM)
> 각 테스트 스크립트가 화면의 UI 요소에 직접 접근하지 않고, `RoulettePage`라는 객체를 통해 간접적으로 제어하도록 설계하여 코드의 중복을 줄이고 유지보수성을 극대화했습니다.

📦 TionRouletteTest
 ┣ 📂 pages
 ┃ ┗ 📜 roulette_page.py   # 화면 요소(Locators) 및 주요 동작(Actions) 모음
 ┣ 📂 tests
 ┃ ┣ 📜 conftest.py        # Appium Driver 초기화 및 셋업/티어다운 로직
 ┃ ┣ 📜 test_mode_a.py     # 공통 로직 및 기본 모드 검증
 ┃ ┣ 📜 test_mode_b.py     # 서바이벌 모드 전용 검증
 ┃ ┣ 📜 test_mode_c.py     # 커스텀 확률 모드 전용 검증
 ┃ ┗ 📜 test_preset.py     # 데이터 저장 및 복구(프리셋) 검증

## Key Test Scenarios & Coverage
Full TC: [Roulette_Testsuit](https://docs.google.com/spreadsheets/d/e/2PACX-1vQhfKgoulnXGsKzU27oW8cVXLnvv9xbmZtBpArXROjRXamM5n7OGvxu8kdv9H1nkJhDt1kyCU9LNZa5/pubhtml)

이 프로젝트는 단순한 해피 패스(Happy Path) 검증을 넘어, 모바일 앱 환경에서 발생할 수 있는 다양한 예외 상황에 대한 방어 로직을 꼼꼼하게 검증합니다.

| 분류 | 주요 검증 시나리오 (Test Cases) |
| --- | --- |
| **공통 (Mode A)** | - 최소 항목(2개) 미만 삭제 시 방어 로직 작동 확인<br>- 빈 텍스트("") 입력 시 스핀 버튼 비활성화 검증<br>- 스핀 버튼 중복 클릭(따닥) 방어 검증 |
| **서바이벌 (Mode B)** | - 룰렛 결과에 따른 당첨 항목 비활성화(Dim) 및 재스핀 제외 검증<br>- 모든 항목 당첨 완료 후 상태 자동 초기화 및 무결성 검증 |
| **확률/가챠 (Mode C)** | - 소수점 둘째 자리(n.nn%) 초과 입력 시 정규식 마스킹 방어 검증<br>- 0% 확률 입력 시 동적 렌더링 및 당첨 풀(Pool) 제외 확인<br>- 확률 총합 부동소수점 오차(99.99%, 100.01%) 시 스핀 방어 검증 |
| **데이터 무결성** | - 현재 룰렛 상태(메뉴명, 커스텀 확률) 프리셋 저장 및 동적 덮어쓰기 분기 처리 검증<br>- 데이터 임의 훼손 후 프리셋 불러오기를 통한 UI/데이터 완벽 복구 검증 |

## Troubleshooting (주요 트러블슈팅)

**1. Jetpack Compose 접근성 트리 동기화(State Sync) 이슈 해결**
- **문제:** Compose UI 특성상 버튼의 활성화/비활성화 상태(`enabled`)가 변경될 때 Appium이 이를 즉각적으로 인식하지 못하거나 과거의 캐시 된 속성을 반환하는 버그 발생.
- **해결 방안:** 앱 개발 코드(Kotlin)에 개입하여 UI 컴포넌트 상태에 따라 변하는 **동적 ID(Stateful ID)** 적용 (예: `btn_spin_enabled`, `btn_spin_disabled`). Appium이 요소의 속성(Attribute)을 우회 검사하는 대신, 화면 내 특정 ID의 **존재 여부(Presence)**를 스캔하도록 검증 로직을 고도화하여 테스트의 견고함(Robustness) 확보.

**2. 텍스트 지우기 버그(Silent Fail) 우회**
- **문제:** Appium의 `.clear()` 함수가 Compose의 `OutlinedTextField`에서 에러 없이 무시되는 현상 발생.
- **해결 방안:** 키보드 커서를 강제로 맨 뒤로 이동(`KEYCODE_MOVE_END`)시킨 후, 물리적인 백스페이스(`KEYCODE_DEL`) 이벤트를 반복 전송하는 **물리적 텍스트 삭제 로직**을 구현하여 완벽한 데이터 초기화 및 교체 성공.

## How to Run

해당 자동화 테스트를 실행하기 위한 명령어입니다.

```bash
# 전체 테스트 슈트 한 번에 실행 (추천)
python -m pytest tests/ -v -s

# 특정 모드만 단독으로 실행하고 싶을 때
python -m pytest tests/test_mode_a.py -v -s
python -m pytest tests/test_mode_b.py -v -s
python -m pytest tests/test_mode_c.py -v -s
python -m pytest tests/test_preset.py -v -s
