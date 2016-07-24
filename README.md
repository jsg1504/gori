# gori-server, use django

## 고리는 사용자간 사진을 공유하는 서비스입니다.
### Play Store : https://play.google.com/store/apps/details?id=com.mozible.gori
<img src="https://github.com/jhlee789/gori-android/blob/master/graphic_image.png" width="90%">

### 고리 서버에서 구현된 기능은 다음과 같습니다.

> User 관련 기능

>> Login POST

>> Logout POST

>> 특정 유저 정보 GET

>> 특정 유저 디테일 정보 GET

>> 내 정보 GET

>> 회원가입 POST

>> 회원가입시 이메일 인증 연동

>> 특정 위치의 사용자 정보 GET

>> 내 정보 UPDATE POST

>> 내 프로필 이미지 UPDATE POST

>> FOLLOW POST

>> UNFOLLOW POST

>> FOLLOWER GET

>> FOLLOWING GET

>> search by username GET

> 게시물 관련 기능

>> 새로운 게시물 올리기 POST

>> 게시물 올리기 취소 POST

>> 게시물 상세 정보 요청 GET

>> 특정 유저의 게시물 받아오기 GET

>> 최근 올라온 게시물 받아오기 GET

>> FOLLOWING하고 있는 사람을 기반으로 게시물 받아오기 GET

> DB와 연동되는 CMS(관리시스템 구축), use django admin