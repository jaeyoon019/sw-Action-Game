# Mermaid 예시

```mermaid
graph TD
    A[시작] --> B{조건 확인}
    B -->|Yes| C[작업 수행]
    B -->|No| D[종료]
    C --> D
