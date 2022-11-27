# foodiary
## 1. 프로젝트 개요
  ### 👧 인력구성
  + 개인프로젝트
  ### 🪄 프로젝트 목적
  + 쿠팡 상품의 경우 매일 상품의 가격이 달라집니다. <br>
    상품 구매 직후 가격이 인하하여 안타까운적이 있습니다.<br>
    가격 변동 추이를 파악하여 구매하려는 상품의 시세를 보여주어 구매시기 결정에 도움을 줄 수 있습니다. <br>
    또한 등록한 상품 중심으로 커뮤니티를 만들어 가격정보 이외에 정보를 공유할 수 있습니다. <br>
   ### ⚙️ 환경
   + ``` python3.8 ```
   + **Framework** :Django
   + **Database** : sqlite | RDB-Mysql
   + **OS** : window | EC2-Linux
  
 
## 2. 기능
  + **회원가입**<br>
    User 모델의 objects.create_user기능을 이용하여 유효성 검사와 저장을 한번에 수행<br>
  + **로그인 & 로그아웃**<br>
    + **detail**<br>
      django.contrib.auth의 authenticate을 이용하여 DB의 회원정보와 대조하여  로그인을 유지합니다.<br>
      `login()`  함수를 통해 세션데이터를 데이터베이스의 **세션 테이블**에 저장합니다<br>
      
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
      <img src=https://user-images.githubusercontent.com/59391473/204123286-7d19c1ca-0955-4da5-8117-a9124cf2c785.png width="500" height="200"/>
      <img src=https://user-images.githubusercontent.com/59391473/204123271-dbd6c817-b0d4-4ad7-9ff3-5a360cc10916.png width="300" height="250"/>
    + **detail**<br>
      selenium을 이용한 크롤링으로 쿠팡 장바구니 속 상품의 정보를 가져옵니다.<br> 
      
      이용자들의 장바구니 속 상품을 모두 product 테이블에 중복되는 크롤링을 방지했습니다. <br>
      이때 상품별로 이용자 테이블을  One-to-many의 관계로 생성하여 자신의 장바구니에 담긴 상품만 조회 가능하도록 했습니다.<br>
      job에 등록하여 3 시간에 한번 크롤링하며 하루의 최저 금액을 저장하고 일별 최저가를 보여줍니다.<br>

  + **블로그**<br>
    + **ERD**<br>
      <img src=https://user-images.githubusercontent.com/59391473/204120438-cc95fe4b-114b-4273-aca6-6bf8b067cfd9.png width="300" height="300"/>
      <img src=https://user-images.githubusercontent.com/59391473/204120494-9f34aaee-8032-42d2-a888-5f1c49996432.png width="300" height="250"/>
      <img src=https://user-images.githubusercontent.com/59391473/204120533-f7d44137-bbcd-41ec-bc38-458210a016a2.png width="300" height="250"/><br>
      
    + **detail**<br>  
      product 테이블에 있는 상품을 one to one 으로 연결하여 해당 주제의 글을 쓸 수 있습니다.
      post와 comment, liker를 one-to-many 관계로 구현했습니다<br>
      django 의 orm 을 이용하여 유저가 댓글을 달거나 좋아요를 누른 글을 역참조 할수 있습니다<br>




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