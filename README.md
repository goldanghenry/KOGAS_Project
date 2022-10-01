# KOGAS_Project
## KOGAS_Project
--------------------------------------------------------------------------------------------<br>

### < 지난 작업 >
1. flask 웹 서버 구축
2. excel to html 변환 test
3. 관리자 회원가입 및 로그인
4. 간이공사 추가
5. 공사 페이지 동적 라우팅 및 자동 완성
6. 웹의 계약서에서 수정 및 저장 기능 test

### < 현재 진행중인 작업 >
1. 페이지 생성 및 링크 작업
2. 업체 비밀번호 확인 로직

### < 해야할 작업 >
1. 계약 단계 입력 창 양식 및 DB쿼리 수정
2. 파일 업로드

--------------------------------------------------------------------------------------------<br>
### < 오리엔테이션 >
: 많이 만들기 보다는 기대효과적인 측면에서 방향을 설정해서 개발. 완성도가 높으면 수의계약도 가능

### < 컨설팅 방향 >
: 실제 운영할 때 문서들이 현행화를 어떻게? 양식이 변경되는 경우 어떻게 유지보수를 할 지.

### < 문서 >
* 공통
1. 메인페이지 : index.html
2. 개요 : summary.html
3. 공지사항 : notice.html
4. 용역 현황 : serviceStatus.html
5. 공사 리스트 생성 페이지 : createConstruction.html
6. 관리자용 로그인&회원가입 페이지 : login.html

* 업체
1. 업체 비밀번호 확인 : pre.html
  : index.html -> pre/<계약번호> -> myPage.html
2. 업체 홈(현황 한 눈에 보기) : myPage.html

3. 계약 단계 개요 : contractPhase.html
1) 기본 정보 입력 : contractInput.html
2) 필요 서류 다운로드 및 업로드 : contractDownload.html
	: 해당 서류 페이지는 contract1 부터 시작

4. 착공 단계 개요 : startPhase.html
1) 기본 정보 입력 : startPhaseInput.html
2) 필요 서류 다운로드 및 업로드 : startPhaseDownload.html
	: 해당 서류 페이지는 start1 부터 시작

5. 준공 단계 개요 : completionPhase.html
1) 기본 정보 입력 : completionInput.html
2) 필요 서류 다운로드 및 업로드 : completionDownload.html
	: 해당 서류 페이지는 completion1 부터 시작

### < 계약 단계 입력 데이터 >
(kogas)
계약 번호 - 공사명 - 사업장 - 업체명
공사감독명 , 연락처(감독)
계약금액(VAT 제외), 계약보증금율, 하자보증금율

(업체)
계약 번호
공사명
계약금액(VAT 제외)
계약일 , 계약기간
업체명 , 대표자 성명
사업자등록번호 , 법인등록번호
업체 연락처 , 팩스번호
계약업체 주소
은행명 , 예금주명 , 계좌번호