# foodiary
## 1. 프로젝트 개요
  ### 👧 인력구성
  + 개인프로젝트
  ### 🪄 프로젝트 목적
  + 쿠팡 상품의 경우 매일 상품의 가격이 달라진다. <br>
    가격 변동을 한눈에 파악하기 어려워 구매 시기 결정에 어려움이 있다.<br>
    가격을 기록하여 적절한 시기를 판별할 수 있도록 도움을 주는 api를 제공한다.<br>
    또한 등록한 상품 중심으로 커뮤니티를 만들어 정보 획득이 쉽게한다. 
   ### ⚙️ 환경
   + ``` python3.8 ```
   + **Framework** :Django
   + **Database** : sqlite | RDB-Mysql
   + **OS** : window | EC2-Linux
  
 
## 2. 기능
  + **회원가입**<br>
    User 모델의 objects.create_user기능을 이용하여 유효성 검사와 저장을 한번에 수행<br>
  + **로그인 & 로그아웃**<br>
    + **구현**<br>
      django.contrib.auth의 authenticate을 이용하여 DB의 회원정보와 대조하여  로그인을 유지합니다.
      + 접근 권한 관리<br>
        Permission을 커스텀하여 회원과 비회원의 기능을 구분할 수 있습니다.<br>
        SessionAuthentication 을 이용 신원 확인 후 권한을 부여합니다.<br>
 

        |user|Permission Class|Available|
        |---|---|---|
        |no login|ReadOnly|읽기 가능|
        |login|IsAuthenticated|읽기 & 쓰기 가능|
        |login&owner|IsOwnerOrReadOnly |읽기 & 쓰기 & 해당 게시글 수정 가능|
      

  + **쿠팡 장바구니 상품 가격 저장**<br>
    + **ERD**<br>
   
    + **구현**<br>
      selenium을 이용한 크롤링으로 쿠팡 장바구니 속 상품의 정보를 가져옵니다.<br> 
      이때 상품별로 이용자 테이블을  One-to-many의 관계로 생성했습니다.<br>
      이용자가 같은 상품을 담았을 때에 데이터가 중복되는 문제를 해결하고, <br>
      상품 정보를 공유하여 메모리를 아낄 수 있었습니다.<br>
      job에 등록하여 일정 주기마다 크롤러를 작동시켰습니다. <br>
      세시간에 한번 크롤링하며 하루의 최저 금액을 저장하고 CanvasJS를 이용하여 가격 변동 추이를 시각화 .<br>

  + **블로그**<br>
    + **ERD**<br>
      <img src=https://user-images.githubusercontent.com/59391473/203903745-8ca07e09-2a67-4826-affd-2b6f7f05f844.png width="300" height="250"/>
      <img src=https://user-images.githubusercontent.com/59391473/203904305-e08db222-32bd-47ac-a024-eee281db7c5f.png width="300" height="250"/>
      <img src=https://user-images.githubusercontent.com/59391473/203904195-17b3c210-abc4-4d07-bb5b-fe8a889169f5.png width="300" height="250"/><br>
    + **구현**<br>  
      댓글 기능<br>
      post와 comment 를 one-to-many 관계로 생성<br>

      좋아요 기능<br>
      post 와 liker를 one-to-many 관계로 구현<br>
      django 의 orm 을 이용하여 유저가 댓글을 달거나 좋아요를 누른 글을 역참조 할수 있음<br>


  <details>
  <summary>주요코드</summary>
  <div markdown="1">   
   ```
    blah
   ```
  </div>
  </details>
  


## 3. 사용 기술 
  + **3. 1. stack 🔧**<br>
    + <img src="https://img.shields.io/badge/Django-092E20?style=flat&logo=Django&logoColor=white"/><img src="https://img.shields.io/badge/Mysql-4479A1?style=flat&logo=Mysql&logoColor=white"/><img src="https://img.shields.io/badge/SQlite-003B57?style=flat&logo=SQLite&logoColor=white"/>
<img src="https://img.shields.io/badge/AmazonEC2-FF9900?style=flat&logo=AmazonEC2&logoColor=white"/><img src="https://img.shields.io/badge/Gunicorn-499848?style=flat&logo=Gunicorn&logoColor=white"/><img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=Python&logoColor=white"/><img src="https://img.shields.io/badge/NGINX-009639?style=flat&logo=NGINX&logoColor=white"/>

  + **3. 2.  tool ⚙**<br>
    + <img src="https://img.shields.io/badge/VisualStudio-5C2D91?style=flat&logo=VisualStudio&logoColor=white"/><img src="https://img.shields.io/badge/Github-181717?style=flat&logo=Github&logoColor=white"/>

## 4. 개발 🗓📆
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


## 5. URL 명세
  + **5. 1. /account**

|CRUD|HTTP|URL|
|---|---|---|
|로그인|POST|/login|
|로그아웃|GET|/logout|
|회원가입|POST|/register|
|카카오 회원가입|GET|/kakao/login|

  + **5. 2. /blog**

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


## 6. UML 명세🧾🗂
  + **6. 1. 클래스 다이어그램**<br>
    <img src=https://user-images.githubusercontent.com/59391473/203677507-6b3c0f3f-c783-4cb3-bb4a-e6a733b1ff17.png width="700" height="500"/><br>


  + **6. 2 시퀀스 다이어그램**<br>
    + **6. 2. 1. 장바구니 상품 update 시퀀스 다이어그램**<br>
    <img src=https://user-images.githubusercontent.com/59391473/203673980-6683036e-cd72-482f-953d-cf48655a744d.png width="700" height="500"/><br>

    + **6. 2. 2. 로그인 시퀀스 다이어그램**<br>
    <img src=https://user-images.githubusercontent.com/59391473/203673983-2c1ab92b-7674-45dd-9426-b025b2b1d46a.png width="700" height="500"/><br>

## 7. Trouble Shooting
  ### 7.1 상품 데이터 중복 이슈
  **문제**
   ![image](https://user-images.githubusercontent.com/59391473/203907074-d7436b9d-d557-46e4-bc9f-bfc6c41fc3fd.png)<br>  
    + 서로 다른 이용자가 같은 상품을 담았을 때 상품 정보가 중복되어 데이터베이스 낭비가 발생<br>

  **해결**
   ![image](https://user-images.githubusercontent.com/59391473/204101651-0f42324b-d661-4312-80f7-f6ebe3180aed.png)
    + 사용자의 장바구니를 주기적으로 크롤링하여 업데이트 하던 방식에서 사용자들의 장바구니에 있는 상품을 url 과 함께 product 모델에 저장했다.<br>
      이후 상품가격 정보를 업데이트 할 때에는 product의 url로 사이트에 접속하여 정보를 가져올 수 있었다.
      이용자마다 크롬드라이버를 열어 로그인하고 크롤링하던 과정을 로그인 없이 한번에 할 수 있는 효과도 있었다.
  ### 7.2 CanvasJS 데이터 포맷 이슈

