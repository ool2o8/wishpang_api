# foodiary

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

###
클래스 다이어그램
![wishpangclassdiagram](https://user-images.githubusercontent.com/59391473/203677507-6b3c0f3f-c783-4cb3-bb4a-e6a733b1ff17.png)


### 장바구니 상품 update 시퀀스 다이어그램
![Untitled (2)](https://user-images.githubusercontent.com/59391473/203673980-6683036e-cd72-482f-953d-cf48655a744d.png)

### 로그인 시퀀스 다이어그램
![Untitled (3)](https://user-images.githubusercontent.com/59391473/203673983-2c1ab92b-7674-45dd-9426-b025b2b1d46a.png)
