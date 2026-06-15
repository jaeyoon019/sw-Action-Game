# MVP 스펙 문서

> 본 프로젝트의 **MVP만**을 정의한다. 다른 문서(클래스 다이어그램, 유스케이스, UI 설계서)는 최종 비전을 그린 것이며, **MVP 구현 단계에서는 이 문서가 유일한 기준**이다.
> 팀원이 AI에 구현을 요청할 때는 항상 이 문서를 함께 첨부한다.

---

## 1. MVP 한 줄 정의

**한 개의 횡스크롤 스테이지를 시작 지점에서 클리어 지점까지 키보드로 통과할 수 있는 게임.**

플레이어는 이동/점프로 지형과 트랩을 피해 골(Goal)에 도달한다. 사망 시 마지막 체크포인트에서 즉시 재시작한다.

---

## 2. 범위 (Scope)

### 2.1 MVP에 포함

- 좌/우 이동, 점프
- 중력 / 낙하 / 최대 낙하 속도
- 정적 지형(플랫폼) AABB 충돌
- 1종 이상의 트랩 (예: 스파이크 = 닿으면 즉시 사망)
- 낙사 (y가 일정 값 초과 시 사망)
- 체크포인트 1개 이상
- 사망 시 마지막 체크포인트에서 즉시 재시작
- 1개 스테이지 + 클리어 시 단순 텍스트 "STAGE CLEAR"
- 메뉴 화면 → 게임 → 클리어 → 메뉴 흐름

### 2.2 MVP에 **포함하지 않음** (AI에 시키지 말 것)

다음은 모두 후속 단계의 비전 문서에만 존재한다. **MVP 구현 코드에 절대 포함하지 않는다.**

- 회원가입 / 로그인 / User / Admin
- 인벤토리 / 아이템 / 장비 / 소비아이템
- 상점 / 골드
- 점수 / 랭킹 / 도전 과제
- 세이브 / 로드 / SaveData
- 레벨업 / 경험치 / 스킬 / MP
- 몬스터 / 보스 / 적 AI
- 사운드 (있어도 되지만 DoD 아님)
- 게임 패드 지원 (키보드만)
- 멀티 스테이지 (1개만)

> AI 프롬프트 시 위 목록을 그대로 던지고 **"이 항목은 추가하지 말 것"** 이라 명시한다.

---

## 3. 기술 스택 (확정)

| 항목 | 선택 | 비고 |
|------|------|------|
| 언어 | Python 3.11+ | 팀원 전원 동일 버전 |
| 게임 라이브러리 | **pygame-ce** | `pip install pygame-ce` (일반 pygame 아님) |
| 타일맵 에디터 | **Tiled** | https://www.mapeditor.org |
| 타일맵 로더 | **pytmx** | `pip install pytmx` |
| 충돌 판정 | `pygame.Rect` (AABB) | pymunk / box2d 금지 |
| 의존성 관리 | `requirements.txt` | 루트 |
| 실행 | `python src/main.py` | 한 줄 |

---

## 4. 폴더 구조 (확정)

```
sw-Action-Game/
├── src/
│   ├── main.py          # 진입점 + 게임 루프
│   ├── settings.py      # 모든 상수
│   ├── scenes/
│   │   ├── __init__.py
│   │   ├── scene.py     # Scene 베이스
│   │   ├── menu.py
│   │   └── gameplay.py
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── player.py
│   │   ├── trap.py
│   │   └── checkpoint.py
│   └── systems/
│       ├── __init__.py
│       ├── stage.py
│       └── camera.py
├── assets/
│   ├── sprites/
│   ├── tilemaps/        # .tmx 파일
│   └── sounds/
├── requirements.txt
└── README.md
```

각 팀원은 **자기 담당 파일만 수정한다.** 공용 상수 변경이 필요하면 PM에게 요청.

---

## 5. 핵심 상수 (`src/settings.py`에 박아둘 값)

```python
import pygame

# 화면
SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720
FPS           = 60
TITLE         = "Action Game"

# 타일
TILE_SIZE = 16

# 물리 (단위: 픽셀, 초)
GRAVITY            = 1200.0   # px/s^2
PLAYER_SPEED       = 200.0    # px/s  (좌/우)
JUMP_VELOCITY      = -500.0   # px/s  (음수 = 위)
TERMINAL_VELOCITY  = 900.0    # px/s  (최대 낙하 속도)

# 사망 / 리스폰
DEATH_Y = 2000   # 플레이어 y가 이 값 초과 시 낙사

# 키 매핑
KEY_LEFT  = pygame.K_LEFT
KEY_RIGHT = pygame.K_RIGHT
KEY_JUMP  = pygame.K_SPACE
KEY_PAUSE = pygame.K_ESCAPE   # 현재 MVP 미사용 (후속 단계 일시정지 기능 예약)
```

> 모든 이동은 **반드시 dt 기반**:
> `pos += velocity * dt`
> `velocity.y += GRAVITY * dt` (단, `min(velocity.y, TERMINAL_VELOCITY)` 클램프)

---

## 6. 좌표계 / 시간 / 충돌 규칙

- **좌표계**: 화면 좌상단이 (0, 0), x→오른쪽, y→아래
- **단위**: 픽셀(공간), 초(시간)
- **dt**: 메인 루프에서 `dt = clock.tick(FPS) / 1000.0` 으로 산출. 모든 이동/물리에 곱한다
- **충돌**: `pygame.Rect`의 AABB 만 사용
- **분리 축**: 수평 이동 → 수평 충돌 해결 → 수직 이동 → 수직 충돌 해결 (순서 고정)
- **on_ground 판정**: 수직 이동 중 아래 방향 충돌이 발생했을 때만 True

---

## 7. MVP 클래스 명세

MVP에는 **아래 9개 클래스만** 존재한다. (`Scene` 베이스·`MenuScene`·`GameplayScene`을 각각 1개로 계산, §7.2 참조) 클래스 다이어그램의 그 외 클래스(User, Item, Shop, Monster 등)는 만들지 않는다.

### 7.1 `Game` (`src/main.py`)
```python
class Game:
    def __init__(self) -> None: ...
    def run(self) -> None: ...                  # 메인 루프
    def change_scene(self, scene: "Scene") -> None: ...
```
- pygame 초기화, 창 생성, 클럭 관리
- 현재 Scene에 매 프레임 `handle_event` / `update(dt)` / `draw(surface)` 위임
- 우측 상단에 FPS 카운터 디버그 표시 (검증 편의)

### 7.2 `Scene` (베이스) + `MenuScene`, `GameplayScene`
```python
class Scene:
    def handle_event(self, event: pygame.event.Event) -> None: ...
    def update(self, dt: float) -> None: ...
    def draw(self, surface: pygame.Surface) -> None: ...
```
- `MenuScene`: 타이틀 텍스트 + "Press Space to Start". Space → GameplayScene
- `GameplayScene`: Stage 로드, Player 생성, Camera 업데이트, 클리어 시 "STAGE CLEAR" 표시 후 Space로 MenuScene 복귀

### 7.3 `Player` (`src/entities/player.py`)
```python
class Player:
    rect: pygame.Rect
    velocity: pygame.Vector2
    on_ground: bool
    last_checkpoint: pygame.Vector2

    def __init__(self, spawn_x: float, spawn_y: float) -> None: ...
    def handle_input(self, keys) -> None: ...
    def update(self, dt: float, solids: list[pygame.Rect]) -> None: ...
    def draw(self, surface: pygame.Surface, camera_offset: pygame.Vector2) -> None: ...
    def respawn(self) -> None: ...   # last_checkpoint 좌표로 복귀, velocity 0
```
- `handle_input`: 좌/우 키 → `velocity.x`, 점프 키 + `on_ground` → `velocity.y = JUMP_VELOCITY`
- `update`: 중력 적용 → x축 이동/충돌 해결 → y축 이동/충돌 해결 → 낙사(`y > DEATH_Y`) 시 `respawn()`
- 더블 점프 / 대시 / 벽 점프 **없음**

### 7.4 `Stage` (`src/systems/stage.py`)
```python
class Stage:
    solids: list[pygame.Rect]
    traps: list[Trap]
    checkpoints: list[Checkpoint]
    spawn_point: pygame.Vector2
    goal_rect: pygame.Rect
    width: int   # 픽셀
    height: int

    def __init__(self, tmx_path: str) -> None: ...
    def draw(self, surface: pygame.Surface, camera_offset: pygame.Vector2) -> None: ...
```
- Tiled `.tmx`에서 다음 이름 규칙으로 읽는다 (이름 변경 금지):
  - 타일 레이어 `Solid` → `solids`
  - 오브젝트 레이어 `Spawn` → `spawn_point` (단일)
  - 오브젝트 레이어 `Goal` → `goal_rect` (단일)
  - 오브젝트 레이어 `Trap` → `traps`
  - 오브젝트 레이어 `Checkpoint` → `checkpoints`

### 7.5 `Trap` (`src/entities/trap.py`)
```python
class Trap:
    rect: pygame.Rect
    def collides_with(self, player_rect: pygame.Rect) -> bool: ...
    def draw(self, surface: pygame.Surface, camera_offset: pygame.Vector2) -> None: ...
```
- 닿으면 `GameplayScene`이 `player.respawn()` 호출

### 7.6 `Checkpoint` (`src/entities/checkpoint.py`)
```python
class Checkpoint:
    rect: pygame.Rect
    activated: bool
    def activate(self, player: Player) -> None: ...   # player.last_checkpoint 갱신
    def draw(self, surface: pygame.Surface, camera_offset: pygame.Vector2) -> None: ...
```

### 7.7 `Camera` (`src/systems/camera.py`)
```python
class Camera:
    offset: pygame.Vector2
    def update(self, target_rect: pygame.Rect, stage_width: int, stage_height: int) -> None: ...
```
- 플레이어를 화면 중앙에 두는 단순 추적
- 스테이지 경계 밖이 보이지 않도록 offset 클램프

---

## 8. 협업 규칙

- 브랜치: `feature/<영역>` (예: `feature/player`, `feature/stage`)
- main 직접 push 금지, **PR로만 머지**
- PR 머지 전 체크리스트:
  - [ ] 로컬에서 `python src/main.py` 실행 시 에러 없이 메뉴 진입
  - [ ] MVP 제외 항목이 코드에 없음
- AI 사용 시 이 문서 전체를 첨부하고 **"이 스펙 안에서만 구현해줘"** 명시
- AI 사용 기록은 `docs/ai-usage-record/<이름>.md`에 누적

---

## 9. 에셋 정책

- 1순위: **Kenney.nl** CC0 에셋 (Pixel Platformer 팩 권장)
- 2순위: itch.io 무료 에셋 (라이선스 반드시 확인)
- 자체 제작 가능
- 모든 출처는 `docs/CREDITS.md`에 누적 기록 (저작권 안전장치)
- MVP 초기에는 단색 사각형(placeholder)으로 시작해도 무방

---

## 10. 완료 정의 (Definition of Done)

MVP는 다음을 **전부** 만족할 때 완료된 것으로 본다.

- [ ] `pip install -r requirements.txt && python src/main.py` 두 줄로 실행
- [ ] 메뉴 → Space → 게임 플레이 → 골 도달 → "STAGE CLEAR" 표시 → 메뉴 복귀 의 흐름이 끊김 없이 동작
- [ ] 키 입력에 대해 100ms 이내 반응 (QA 측정)
- [ ] 트랩 접촉 또는 낙사 시 마지막 체크포인트에서 즉시 재시작
- [ ] Windows에서 실행 검증
- [ ] 2.2의 제외 항목이 코드에 **하나도 없음**

---

*최종 수정: 2026-06-10 | 담당: 이재윤(PM)*
