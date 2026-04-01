* 프로젝트 소개: Appium으로 자동화를 구축하기 위해 AI를 사용하여 AOS/iOS 앱을 만든 뒤 AI를 사용하여 구축 한 Appium 자동화 프로젝트.
* 테스트 시나리오: [Roulette_Testsuit](https://docs.google.com/spreadsheets/d/e/2PACX-1vQhfKgoulnXGsKzU27oW8cVXLnvv9xbmZtBpArXROjRXamM5n7OGvxu8kdv9H1nkJhDt1kyCU9LNZa5/pubhtml)
* 기술 스택:
* 실행 방법: `python -m pytest tests/`

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
```text
📦 TionRouletteTest
 ┣ 📂 pages
 ┃ ┗ 📜 roulette_page.py   # 화면 요소(Locators) 및 주요 동작(Actions) 모음
 ┣ 📂 tests
 ┃ ┣ 📜 conftest.py        # Appium Driver 초기화 및 셋업/티어다운 로직
 ┃ ┣ 📜 test_mode_a.py     # 공통 로직 및 기본 모드 검증
 ┃ ┣ 📜 test_mode_b.py     # 서바이벌 모드 전용 검증
 ┃ ┣ 📜 test_mode_c.py     # 커스텀 확률 모드 전용 검증
 ┃ ┗ 📜 test_preset.py     # 데이터 저장 및 복구(프리셋) 검증
```

## Key Test Scenarios & Coverage
Full TC: [Roulette_Testsuit](https://docs.google.com/spreadsheets/d/e/2PACX-1vQhfKgoulnXGsKzU27oW8cVXLnvv9xbmZtBpArXROjRXamM5n7OGvxu8kdv9H1nkJhDt1kyCU9LNZa5/pubhtml)

| 분류 | 주요 검증 시나리오 (Test Cases) |
| --- | --- |
| 공통 (Mode A) | - 최소 항목(2개) 미만 삭제 시 방어 로직 작동 확인\n- 빈 텍스트("") 입력 시 스핀 버튼 비활성화 검증
- 스핀 버튼 중복 클릭(따닥) 방어 검증 |
| 모드 B | 서바이벌 모드 팝업 감지 |
| 모드 C | 0% 확률 방어 및 소수점 제한 |
