# 게시판 웹 애플리케이션

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-CC2927?style=for-the-badge&logo=sqlite&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=json-web-tokens&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

회원가입, 로그인, 게시글 CRUD, 댓글 기능을 제공하는 풀스택 웹 애플리케이션입니다. RESTful API를 위한 FastAPI 백엔드와 모던 UI를 위한 Next.js 프론트엔드로 구성되어 있습니다.

## 프로젝트 구조

```
📦 게시판 애플리케이션
├── 📂 backend (FastAPI)
│   ├── 📂 app
│   │   ├── 📂 api         # API 엔드포인트 정의
│   │   ├── 📂 core        # 설정, 보안, 공통 기능
│   │   ├── 📂 db          # 데이터베이스 연결 및 세션 관리
│   │   ├── 📂 models      # SQLAlchemy ORM 모델
│   │   ├── 📂 schemas     # Pydantic 스키마 (데이터 검증)
│   │   └── 📂 services    # 비즈니스 로직
│   ├── 📂 migrations      # Alembic 데이터베이스 마이그레이션
│   └── 📂 tests           # 백엔드 테스트 코드
└── 📂 frontend (Next.js)
    ├── 📂 src
    │   ├── 📂 app         # Next.js App Router 페이지
    │   ├── 📂 components  # 재사용 가능한 컴포넌트
    │   ├── 📂 context     # React Context (전역 상태 관리)
    │   ├── 📂 lib         # API 클라이언트, 유틸리티 함수
    │   └── 📂 types       # TypeScript 타입 정의
    └── 📂 public          # 정적 파일
```

## 주요 기능

### 인증 시스템
- 회원가입 및 로그인
- JWT 기반 인증 (액세스 토큰)
- 인증 상태 관리를 위한 React Context
- 보호된 경로 (인증된 사용자만 접근 가능)

### 게시판
- 게시글 목록 조회 (페이지네이션 지원)
- 게시글 상세 조회 (조회수 증가 기능)
- 게시글 작성, 수정, 삭제 (본인 작성 글만 수정/삭제 가능)

### 댓글
- 게시글별 댓글 목록 조회
- 댓글 작성, 수정, 삭제 (본인 작성 댓글만 수정/삭제 가능)

## 기술 스택

### 백엔드
- **FastAPI**: 빠르고 현대적인 Python 웹 프레임워크
- **SQLAlchemy**: Python SQL 툴킷 및 ORM
- **Pydantic**: 데이터 검증 및 설정 관리
- **Alembic**: 데이터베이스 마이그레이션
- **JWT**: JSON Web Token 기반 인증
- **SQLite**: 개발용 데이터베이스 (실 환경에서는 PostgreSQL로 전환 가능)

### 프론트엔드
- **Next.js**: React 기반 프레임워크
- **TypeScript**: 정적 타입 체킹
- **Tailwind CSS**: 유틸리티 우선 CSS 프레임워크
- **React Context API**: 전역 상태 관리
- **Axios**: API 통신 클라이언트

### 테스트
- **Pytest**: 백엔드 테스트
- **Jest + React Testing Library**: 프론트엔드 테스트

## 설치 및 실행 방법

### 백엔드 설정

1. Poetry 설치 (의존성 관리 도구)
   ```bash
   pip install poetry
   ```

2. 의존성 설치
   ```bash
   poetry install
   ```

3. 데이터베이스 마이그레이션
   ```bash
   poetry run alembic upgrade head
   ```

4. 서버 실행
   ```bash
   poetry run python main.py
   ```
   서버는 http://localhost:8000 에서 실행됩니다.

### 프론트엔드 설정

1. Node.js 설치 (v18 이상)

2. 의존성 설치
   ```bash
   cd frontend
   npm install
   ```

3. 개발 서버 실행
   ```bash
   npm run dev
   ```
   프론트엔드는 http://localhost:3000 에서 실행됩니다.

## 문제 해결 가이드

### 프론트엔드 의존성 문제 해결

Tailwind CSS나 기타 의존성 문제가 발생할 때 완전한 재설치를 통해 해결할 수 있습니다.

#### 완전한 재설치 과정 (개인 개발 시)

```bash
# 1. 개발 서버 중지
pkill -f "next dev"

# 2. 모든 모듈과 캐시 삭제
cd frontend
rm -rf node_modules package-lock.json .next

# 3. npm 캐시 정리
npm cache clean --force

# 4. 완전히 새로 설치
npm install

# 5. 개발 서버 실행
npm run dev
```

#### 협업 시 주의사항

⚠️ **팀 프로젝트에서는 `package-lock.json`을 삭제하면 안됩니다!**

협업 시에는 다음 방법을 사용하세요:

```bash
# package-lock.json은 그대로 두고
npm ci  # package-lock.json 기반으로 정확한 버전 설치

# 또는 캐시만 정리
npm cache clean --force
rm -rf node_modules
npm ci
```

#### Tailwind CSS 문제 해결

Tailwind CSS가 제대로 로드되지 않는 경우:

1. **PostCSS 설정 확인**: `postcss.config.js` 파일 존재 여부
2. **Tailwind CSS 버전**: v4는 불안정하므로 v3 사용 권장
3. **캐시 문제**: 위의 완전한 재설치 과정 실행

## 테스트 실행

### 백엔드 테스트
```bash
poetry run pytest
```

### 프론트엔드 테스트
```bash
cd frontend
npm test
```

## API 문서
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 프로젝트 구현 과정에서 배운 점

- **인증 시스템 설계**: JWT 기반 인증 구현과 보안 고려사항
- **데이터베이스 모델링**: SQLAlchemy ORM을 사용한 관계형 모델 설계
- **프론트엔드-백엔드 통합**: API 통신 및 에러 처리 패턴
- **상태 관리**: Context API를 활용한 전역 상태 관리
- **테스트 자동화**: 백엔드 및 프론트엔드 테스트 코드 작성

## 향후 개선 사항

- 소셜 로그인 추가 (OAuth2)
- 파일 업로드 기능
- 게시글 카테고리 및 태그 기능
- 실시간 알림 시스템
- 검색 기능 고도화
- 반응형 디자인 개선

## 라이센스
MIT License 