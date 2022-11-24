# foodiary
## 1. 사용 기술 
### 1.1   stack 🔧
<img src="https://img.shields.io/badge/Django-092E20?style=flat&logo=Django&logoColor=white"/><img src="https://img.shields.io/badge/Mysql-4479A1?style=flat&logo=Mysql&logoColor=white"/><img src="https://img.shields.io/badge/SQlite-003B57?style=flat&logo=SQLite&logoColor=white"/>
<img src="https://img.shields.io/badge/AmazonEC2-FF9900?style=flat&logo=AmazonEC2&logoColor=white"/><img src="https://img.shields.io/badge/Gunicorn-499848?style=flat&logo=Gunicorn&logoColor=white"/><img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=Python&logoColor=white"/><img src="https://img.shields.io/badge/NGINX-009639?style=flat&logo=NGINX&logoColor=white"/>

### 1.2  tool ⚙
<img src="https://img.shields.io/badge/VisualStudio-5C2D91?style=flat&logo=VisualStudio&logoColor=white"/><img src="https://img.shields.io/badge/Github-181717?style=flat&logo=Github&logoColor=white"/>

## 2. 개발 🗓📆
* 2022.06.26 개발환경 셋팅, 장고 앱 생성
* 2022.07.04 DRF-simplejwt로 로그인 구현 
>(django v ersion4 이상에서는 DRF-jwt X)
* 2022.07.05 kakao login api 연결 (account\login view 작성)
* 2022.07.06 kakao login 유저 정보 불러오기->회원가입에 이용
* 2022.07.07 User 모델 확장- OneToOne profile 모델 생성, 비밀번호 해싱, 패키징 관리
* 2022.07.08 ~ 9 session authentication으로 로그인, 
* 2022.07.26 Wishpang 프로젝트 - 쿠팡 장바구니 상품 가격비교, 백그라운드 함수 호출 구현 중
permmition class 지정  permmition class 지정
* 2022-07-27 상품 가격 비교 뷰 작성 -ing
* 2022-07-28 상품 최저가 필터링
* 2022-07-31 aws rds 데이터 베이스 연결
## 3. URL 
* /account/

|CRUD|HTTP|URL|
|---|---|---|
|로그인|POST|/login|
|로그아웃|GET|/logout|
|회원가입|POST|/register|
|카카오 회원가입|GET|/kakao/login|

* /blog/

|CRUD|HTTP|URL|
|---|---|---|
|게시글 조회|GET|/post|
|게시글 등록|POST|/post|
|특정 게시글 조회|GET|/post/{post_id: int}|
|내 게시글 조회|GET|/user-post|
|해당 게시글 댓글 조회|GET|/post/{post_id: int}/comment|
|해당 게시글 댓글 등록|POST|/post/{post_id: int}/comment|
|해당 게시글 좋아요|GET|/post/{post_id: int}/like|
|해당 게시글 좋아요 회원 조회|GET|/post/{post_id: int}/like-list|
|쿠팡 장바구니 상품|GET|/my-wish|
|쿠팡 장바구니 상품 가격 조회|GET|/wish-price|
|쿠팡 장바구니 상품 업데이트|GET|/my-wish/update|


## 4. UML 🧾🗂
### 4.1 클래스 다이어그램 
![wishpangclassdiagram](https://user-images.githubusercontent.com/59391473/203677507-6b3c0f3f-c783-4cb3-bb4a-e6a733b1ff17.png)


### 4.2 장바구니 상품 update 시퀀스 다이어그램
![Untitled (2)](https://user-images.githubusercontent.com/59391473/203673980-6683036e-cd72-482f-953d-cf48655a744d.png)

### 4.3 로그인 시퀀스 다이어그램
![Untitled (3)](https://user-images.githubusercontent.com/59391473/203673983-2c1ab92b-7674-45dd-9426-b025b2b1d46a.png)
