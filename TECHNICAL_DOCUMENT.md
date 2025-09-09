# 게시판 애플리케이션 기술 문서

이 문서는 게시판 애플리케이션의 기술적 구현 내용과 각 기술 선택의 이유를 설명합니다.

## 1. 기술 스택 선택 이유

### 1.1 백엔드

#### FastAPI
- **사용 이유**: 
  - 높은 성능과 비동기 지원으로 빠른 API 응답 속도 제공
  - 자동 문서화 기능 (Swagger, ReDoc)으로 API 테스트 및 개발 효율성 향상
  - Pydantic 통합으로 데이터 검증을 간소화
  - Python 3.6+ 타입 힌팅을 활용한 코드 가독성 및 유지보수성 향상
- **적용 위치**: 모든 API 엔드포인트 구현 (`app/api/endpoints/`)

#### SQLAlchemy
- **사용 이유**: 
  - 강력한 ORM으로 SQL 쿼리 없이 객체 지향적 데이터베이스 조작
  - 다양한 데이터베이스 백엔드 지원으로 확장성 보장
  - 데이터베이스 모델과 비즈니스 로직 분리 용이
- **적용 위치**: 데이터베이스 모델 정의 (`app/models/`) 및 쿼리 작성 (`app/services/`)

#### Pydantic
- **사용 이유**: 
  - 런타임 타입 검증 및 데이터 변환 기능 제공
  - API 요청/응답 데이터 자동 검증
  - 설정 관리 단순화
- **적용 위치**: API 스키마 정의 (`app/schemas/`) 및 설정 관리 (`app/core/config.py`)

#### JWT 인증
- **사용 이유**: 
  - 상태를 저장하지 않는(Stateless) 인증 방식으로 서버 확장성 향상
  - 토큰 기반 인증으로 여러 서비스 간 인증 공유 가능
  - 클라이언트 사이드 저장으로 서버 부하 감소
- **적용 위치**: 인증 모듈 (`app/core/security.py`) 및 API 종속성 (`app/api/deps.py`)

#### PostgreSQL
- **사용 이유**: 
  - 벡터 데이터베이스 지원 (pgvector 확장)
  - AI 기능을 위한 임베딩 저장 및 유사도 검색
  - 확장성과 성능이 뛰어난 관계형 데이터베이스
  - 프로덕션 환경에 적합한 안정성
- **적용 위치**: 데이터베이스 연결 설정 (`app/db/session.py`)

#### Alembic
- **사용 이유**: 
  - SQLAlchemy와 통합된 데이터베이스 스키마 관리 도구
  - 데이터베이스 스키마 변경사항 버전 관리 가능
  - 롤백 및 마이그레이션 자동화
- **적용 위치**: 데이터베이스 마이그레이션 스크립트 (`migrations/`)

### 1.2 프론트엔드

#### Next.js
- **사용 이유**: 
  - 서버 사이드 렌더링(SSR)과 정적 사이트 생성(SSG) 지원으로 SEO 및 초기 로딩 성능 향상
  - 파일 기반 라우팅으로 개발 복잡성 감소
  - React 기반으로 컴포넌트 재사용성 극대화
  - API 라우트 기능으로 백엔드 API 프록시 가능
- **적용 위치**: 전체 프론트엔드 아키텍처 (`frontend/src/app/`)

#### TypeScript
- **사용 이유**: 
  - 정적 타입 체킹으로 런타임 오류 감소
  - 코드 자동 완성 및 리팩토링 도구 지원 강화
  - 컴파일 타임 오류 감지로 버그 조기 발견
- **적용 위치**: 모든 프론트엔드 코드 (`frontend/src/`)

#### React Context API
- **사용 이유**: 
  - Redux와 같은 추가 라이브러리 없이 전역 상태 관리 가능
  - 컴포넌트 트리 전체에 데이터 전달 용이
  - 간단한 앱 구조에 적합한 복잡성
- **적용 위치**: 인증 상태 관리 (`frontend/src/context/AuthContext.tsx`)

#### Tailwind CSS
- **사용 이유**: 
  - 유틸리티 우선 접근 방식으로 커스텀 디자인 빠르게 구현
  - 적은 CSS 파일 크기로 성능 최적화
  - 컴포넌트 단위 스타일링으로 일관성 유지
- **적용 위치**: 모든 UI 컴포넌트 (`frontend/src/components/`)

#### Axios
- **사용 이유**: 
  - 브라우저 호환성 보장 및 일관된 API
  - 인터셉터를 통한 요청/응답 전처리 기능
  - 에러 처리 단순화
- **적용 위치**: API 클라이언트 (`frontend/src/lib/api.ts`)

## 2. 아키텍처 설계

### 2.1 백엔드 아키텍처
백엔드는 계층화된 아키텍처로 구성되어 있습니다:

1. **API 계층**: FastAPI 라우터 및 엔드포인트
   - 엔드포인트 정의 및 요청/응답 처리
   - 의존성 주입을 통한 인증 및 권한 체크
   
2. **서비스 계층**: 비즈니스 로직
   - CRUD 작업 및 도메인 규칙 구현
   - 트랜잭션 관리
   
3. **모델 계층**: 데이터베이스 모델 및 ORM
   - SQLAlchemy 모델 정의
   - 관계 설정 및 제약 조건

4. **스키마 계층**: 데이터 검증 및 직렬화
   - Pydantic 모델 정의
   - API 요청/응답 스키마

### 2.2 프론트엔드 아키텍처
프론트엔드는 컴포넌트 기반 아키텍처로 구성되어 있습니다:

1. **페이지 컴포넌트**: Next.js 페이지
   - 라우팅 및 페이지 레이아웃 정의
   - 데이터 페칭 및 상태 관리
   
2. **UI 컴포넌트**: 재사용 가능한 컴포넌트
   - 프레젠테이션 로직
   - Tailwind CSS 스타일링
   
3. **상태 관리**: React Context
   - 인증 상태 및 사용자 정보 관리
   - 전역 상태 및 공유 로직
   
4. **API 클라이언트**: Axios 인스턴스
   - 백엔드 API 통신
   - 인터셉터를 통한 토큰 관리 및 에러 핸들링

## 3. 데이터베이스 설계

### 3.1 ERD (Entity Relationship Diagram)

```
+-------------+       +-------------+       +-------------+
|    User     |       |    Post     |       |   Comment   |
+-------------+       +-------------+       +-------------+
| id          |       | id          |       | id          |
| email       |       | title       |       | content     |
| username    |       | content     |       | user_id     |
| hashed_pwd  |<------|>user_id     |       | post_id     |
| is_active   |       | view_count  |<------| created_at  |
| is_admin    |       | created_at  |       | updated_at  |
| created_at  |       | updated_at  |       |             |
| updated_at  |       |             |       |             |
+-------------+       +-------------+       +-------------+
```

### 3.2 모델 관계
- **User** ↔ **Post**: 일대다 관계 (사용자는 여러 게시글 작성 가능)
- **User** ↔ **Comment**: 일대다 관계 (사용자는 여러 댓글 작성 가능)
- **Post** ↔ **Comment**: 일대다 관계 (게시글은 여러 댓글 포함 가능)

## 4. API 설계

### 4.1 RESTful 설계 원칙
- 리소스 기반 URL 구조
- HTTP 메소드를 통한 작업 표현 (GET, POST, PUT, DELETE)
- 상태 코드를 통한 응답 상태 표현

### 4.2 API 엔드포인트
- **인증**: `/api/v1/auth/`
  - `POST /login`: 로그인 및 토큰 발급
  - `POST /register`: 회원가입

- **사용자**: `/api/v1/users/`
  - `GET /me`: 현재 사용자 정보 조회
  - `PUT /me`: 현재 사용자 정보 수정

- **게시글**: `/api/v1/posts/`
  - `GET /`: 게시글 목록 조회 (페이지네이션)
  - `POST /`: 게시글 작성
  - `GET /{id}`: 게시글 상세 조회
  - `PUT /{id}`: 게시글 수정
  - `DELETE /{id}`: 게시글 삭제
  - `GET /{id}/comments`: 게시글 댓글 조회

- **댓글**: `/api/v1/comments/`
  - `POST /`: 댓글 작성
  - `PUT /{id}`: 댓글 수정
  - `DELETE /{id}`: 댓글 삭제

## 5. 인증 시스템

### 5.1 백엔드 인증
- **JWT 토큰** 기반 인증 시스템
- **액세스 토큰** 중심의 간단한 구현
- 비밀번호 해싱에 **bcrypt** 알고리즘 사용
- **Dependency Injection**을 통한 보호된 엔드포인트 구현

### 5.2 프론트엔드 인증
- **AuthContext**를 통한 인증 상태 관리
- **localStorage**에 토큰 저장
- **Axios 인터셉터**를 통한 자동 토큰 첨부
- 401 응답 시 자동 로그아웃 처리

## 6. 기술적 과제 및 해결책

### 6.1 조회수 중복 증가 문제
- **문제**: 동일 사용자가 페이지를 새로고침할 때마다 조회수 증가
- **해결책**: 
  - 세션 스토리지를 활용한 이미 조회한 게시글 추적
  - API에 `skip_increment` 쿼리 파라미터 추가
  - 일정 시간(1시간) 내 재방문 시 조회수 증가 방지

```typescript
// 프론트엔드 - 조회 추적 구현
const visited = sessionStorage.getItem(`visited_post_${postId}`);
const skipIncrement = visited === 'true';
const response = await postAPI.getPost(postId, skipIncrement);
sessionStorage.setItem(`visited_post_${postId}`, 'true');
```

```python
# 백엔드 - 조회수 증가 로직
@router.get("/{post_id}")
def read_post(
    post_id: int,
    skip_increment: bool = Query(False)
):
    # 조회수 증가 로직
    if not skip_increment:
        post = services.post.increment_view_count(db=db, db_obj=post)
    return post
```

### 6.2 UI 색상 문제
- **문제**: 다크 모드에서 텍스트 가독성 저하
- **해결책**: 
  - 다크 모드 감지 비활성화
  - 커스텀 CSS 변수 사용으로 일관된 색상 테마 적용
  - 라이트 모드로 고정하여 가독성 보장

```css
/* globals.css */
:root {
  --background: #ffffff;
  --foreground: #171717;
}

body {
  background: var(--background);
  color: var(--foreground);
}
```

### 6.3 React의 Strict Mode로 인한 이중 렌더링
- **문제**: 개발 모드에서 React의 Strict Mode로 인한 컴포넌트 이중 마운트
- **해결책**: 
  - `useRef`를 사용한 API 호출 추적
  - 마운트 시 한 번만 데이터를 가져오도록 보장

```typescript
const fetchedRef = useRef(false);

useEffect(() => {
  if (fetchedRef.current) return;
  fetchedRef.current = true;
  
  // API 호출 로직
  
  return () => {
    fetchedRef.current = false;
  };
}, []);
```

## 7. 테스트 전략

### 7.1 백엔드 테스트
- **단위 테스트**: 서비스 함수 테스트 (Pytest)
- **통합 테스트**: API 엔드포인트 테스트 (FastAPI TestClient)
- **기능 테스트**: 사용자 시나리오 테스트 (Pytest 픽스처 활용)

### 7.2 프론트엔드 테스트
- **컴포넌트 테스트**: UI 렌더링 및 상호작용 (React Testing Library)
- **통합 테스트**: 여러 컴포넌트 상호작용 (Jest)
- **모킹**: 외부 의존성 모킹 (jest.mock)

## 8. 향후 개선 방향

### 8.1 보안 강화
- HTTPS 적용
- CSRF 보호 추가
- 리프레시 토큰 구현
- 로그인 시도 제한 (Rate Limiting)

### 8.2 성능 최적화
- 데이터베이스 인덱싱 최적화
- API 응답 캐싱
- 이미지 최적화
- 코드 스플리팅

### 8.3 기능 확장
- 소셜 로그인 추가
- 파일 업로드 기능
- 실시간 알림 (WebSocket)
- 검색 기능 강화 