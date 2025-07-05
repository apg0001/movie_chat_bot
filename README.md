# movie_chat_bot

영화 추천 및 정보 조회, 예매 기능을 제공하는 Rasa 기반 챗봇입니다.

---

## 프로젝트 개요

이 챗봇은 사용자의 취향(장르, 평점, 플랫폼 등)에 맞는 영화를 추천하고, 영화 정보 검색, 상영 정보 조회, 영화 예매 및 예매 내역 확인 기능을 제공합니다.  
Rasa 프레임워크와 MySQL 데이터베이스를 활용하여 동작합니다.

---

## 핵심 기술

- **Rasa Framework**: 자연어 처리 및 대화형 AI 챗봇 개발
- **MySQL Database**: 영화 정보, 극장 정보, 상영 정보, 예매 정보 관리
- **DIET Classifier**: 의도 분류 및 엔티티 추출
- **Custom Actions**: Python 기반 사용자 정의 액션 구현

---

## 주요 기능

- 영화 추천 (장르, 평점, OTT 플랫폼 등 조건 기반)
- 영화 정보 검색 (제목 기반)
- 상영 정보 조회 (영화/극장/지역 기반)
- 영화 예매 및 예매 내역 확인

---

## 역할 및 기여

### 자연어 처리 모델 개발
- Rasa NLU 파이프라인 구성 및 최적화
- DIET Classifier를 활용한 의도 분류 및 엔티티 추출
- 사용자 의도별 응답 시나리오 설계

### 데이터베이스 설계 및 연동
- MySQL 데이터베이스 스키마 설계
- 영화, 극장, 상영, 예매 정보 테이블 구성
- Python MySQL Connector를 통한 데이터베이스 연동

### 사용자 정의 액션 개발
- 영화 추천 알고리즘 구현
- 영화 정보 검색 기능 개발
- 상영 정보 조회 및 예매 시스템 구현

---

## 데이터베이스 구성

MySQL 데이터베이스(`movie_database`)를 사용하며, 주요 테이블 구조는 다음과 같습니다.

### 1. movies (영화 정보)
| 필드명      | 타입      | 설명         |
|-------------|-----------|--------------|
| ID          | INT       | 영화 고유 ID |
| Title       | VARCHAR   | 영화 제목    |
| Director    | VARCHAR   | 감독         |
| MainActors  | VARCHAR   | 주연 배우    |
| Genre       | VARCHAR   | 장르         |
| Rating      | FLOAT     | 평점         |
| Country     | VARCHAR   | 국가         |
| Platform    | VARCHAR   | OTT 플랫폼   |
| Synopsis    | TEXT      | 시놉시스     |
| AgeLimit    | INT       | 관람 등급    |

### 2. theaters (극장 정보)
| 필드명      | 타입      | 설명         |
|-------------|-----------|--------------|
| theater_id  | INT       | 극장 고유 ID |
| name        | VARCHAR   | 극장명       |
| location    | VARCHAR   | 지역         |

### 3. screenings (상영 정보)
| 필드명         | 타입      | 설명             |
|----------------|-----------|------------------|
| screening_id   | INT       | 상영 고유 ID     |
| ID             | INT       | 영화 ID (FK)     |
| theater_id     | INT       | 극장 ID (FK)     |
| screening_date | DATE      | 상영 날짜        |
| screening_time | TIME      | 상영 시간        |

### 4. reservations (예매 정보)
| 필드명        | 타입      | 설명             |
|---------------|-----------|------------------|
| reservation_id| INT       | 예매 고유 ID     |
| screening_id  | INT       | 상영 ID (FK)     |

---

## 설치 및 실행 방법

### 1. 의존성 설치

```bash
pip install rasa rasa-sdk mysql-connector-python
```

### 2. 데이터베이스 준비

MySQL에 위의 테이블 구조에 맞게 데이터베이스와 테이블을 생성하고, 영화/극장/상영/예매 데이터를 입력합니다.

### 3. 환경설정

- `config.yml`, `domain.yml`, `data/nlu.yml`, `data/stories.yml`, `data/rules.yml` 등 Rasa 표준 설정 파일을 사용합니다.
- `actions/actions.py`에서 DB 접속 정보(`host`, `user`, `password`, `database`)를 실제 환경에 맞게 수정하세요.

### 4. 챗봇 학습 및 실행

```bash
# NLU/스토리 학습
rasa train

# 액션 서버 실행 (별도 터미널)
rasa run actions --port 9000

# 챗봇 서버 실행
rasa shell
```

---

## 결과 및 성과

- 영화 추천 정확도: 사용자 선호도 기반 맞춤형 추천
- 자연어 처리 성능: 다양한 영화 관련 질의에 대한 정확한 응답
- 데이터베이스 연동: 실시간 영화 정보 조회 및 예매 시스템
- 사용자 경험: 직관적인 대화형 인터페이스 제공

---

## 참고

- 챗봇은 Rasa 오픈소스 프레임워크를 기반으로 동작합니다.
- 데이터베이스 연결 정보 및 테이블 구조는 실제 환경에 맞게 조정이 필요합니다.
- 추가적인 기능 및 커스터마이징은 `actions/actions.py`에서 구현할 수 있습니다.
