# Action Game
> 단국대학교 소프트웨어개론 팀 프로젝트 | 2026년 1학기

## 프로젝트 개요
짧은 시간 내 몰입감 있는 전투와 실력 기반 성장을 경험할 수 있는 2D 횡스크롤 액션 게임을 개발한다.  

사용자는 반복 플레이를 통해 자신의 조작 실력을 향상시키며, 다양한 스테이지와 도전 과제를 통해 성취감을 얻을 수 있다.

## 팀 구성
| 이름 | 역할 |
|------|------|
| 이재윤 | PM (팀장) |
| 김남준 | 분석가 |
| 김민재 | 설계자 |
| 김담영 | 개발자 |
| 윤원준 | QA |

## 주요 기능
- 캐릭터 이동 및 점프 조작 시스템
- 체크포인트 기반 즉시 재시작 기능
- 다양한 지형과 트랩이 포함된 스테이지
- 반복 플레이 기반 실력 향상 구조
- 노 데미지 / 제한 시간 등 도전 과제 시스템 *(최종 비전)*

## 마일스톤
- [M1 기획](https://github.com/jaeyoon019/sw-Action-Game/milestone/1)
- [M2 설계](https://github.com/jaeyoon019/sw-Action-Game/milestone/2)
- [M3 구현·보고](https://github.com/jaeyoon019/sw-Action-Game/milestone/3)

## 기술 스택

- Python 3.11+
- [pygame-ce](https://pyga.me/) — 게임 라이브러리
- [pytmx](https://github.com/bitcraft/pytmx) + [Tiled](https://www.mapeditor.org/) — 타일맵 로더 / 에디터

## 실행 방법

```powershell
pip install -r requirements.txt
python src/main.py
```

자세한 구현 규칙은 [MVP 스펙 문서](docs/mvp-spec.md)를 참조.

## 문서

**구현 기준 (MVP)**
- [**MVP 스펙 문서**](docs/mvp-spec.md) — 구현 단계의 단일 기준. AI에 코드를 요청할 때 항상 첨부

**기획 / 설계 (최종 비전 — MVP 스코프 아님)**
- [요구사항 정의서](docs/requirements.md)
- [WBS 및 일정](docs/wbs.md)
- [비용산정](docs/FP_estimation.md)
- [유스케이스 다이어그램](docs/usecase.md)
- [클래스 다이어그램](docs/classdiagram.md)
- [패키지 다이어그램](docs/PackageDiagram.md)
- [유저 인터페이스](docs/ui.md)

**운영**
- [AI 사용 로그](docs/ai-usage-record/)
- [회의록 목록](docs/meetings/)
- [에셋 출처](docs/CREDITS.md)
