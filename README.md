# KOGAS_Project
## KOGAS_Project
--------------------------------------------------------------------------------------------<br>

### < 지난 작업 >
1. flask 웹 서버 구축
2. excel to html 변환 test
3. 관리자 회원가입 및 로그인
4. 간이공사 추가
5. 공사 페이지 동적 라우팅 및 자동 완성
6. 웹 상의 계약서에서 수정 및 저장 기능 test
7. 동적 메뉴구성 수정
8. 페이지 생성 및 링크 작업
9. 업체 비밀번호 확인 로직
10. 계약 단계 입력 창 양식 및 DB쿼리 수정
11. 계약 단계 table 생성 및 새 창에서 계약서 띄우기
12. 웹 계약서에서 두개 이상 수정 후 DB 테스트

### < 현재 진행중인 작업 >
1. 파일 업로드 로직 File upload using Flask without refresh

### < 해야할 작업 >
1. 승인 요청 페이지 -> 북마크처럼 요청 온 리스트를 만들어서 버튼 생성
	리스트 클릭하면 해당 공사 myPage로 이동 -> 승인하러가기 -> 승인 요청 페이지로 이동해 승인 클릭
2. 하자보증금율 등 드랍박스로 수정하고 디폴트는 10%, 직접입력도 넣기
3. 이미 입력한 정보가 있다면 placeholder나 data-default로 표시하기
4. 양식 요청하기
5. 테이블 셀 수직 가운데 정렬

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
7. 업체 비밀번호 확인 : pre.html
  : index.html -> pre/<계약번호> -> myPage.html
8. 업체 메인페이지(현황 한 눈에 보기) : myPage.html

9. 계약 단계 개요 : contractPhase.html
1) 기본 정보 입력 : contractInput.html
2) 필요 서류 다운로드 및 업로드 : contractTable.html
	: 해당 서류 페이지는 contract1 부터 시작

10. 착공 단계 개요 : startPhase.html
1) 기본 정보 입력 : startPhaseInput.html
2) 필요 서류 다운로드 및 업로드 : startPhaseTable.html
	: 해당 서류 페이지는 start1 부터 시작

11. 준공 단계 개요 : completionPhase.html
1) 기본 정보 입력 : completionInput.html
2) 필요 서류 다운로드 및 업로드 : completionTable.html
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
계약일 , 공사기간
업체명 , 대표자 성명
사업자등록번호 , 법인등록번호
업체 연락처 , 팩스번호
계약업체 주소
은행명 , 예금주명 , 계좌번호

### DB table
1. 관리자 유저 리스트 : userList
0)userId 1)userName 2)userPassword

2. 발주기관 자료 : constructionList
0)contractNum(계약번호)    1)title(공사명)     2)department(사업장)    3)company(업체명) 
4)supervisor(공사감독명)   5)s_contact(감독 연락처)
6)contractAmount(계약금액) 7)deposit_rate(계약보증금율)    8)fault_rate(하자보증금율) 
9)progress(진행관리) 
// 0-계약준비, 1-계약정보입력 완료, 2-승인대기, 3-착공정보입력, 4-승인대기, 5-준공정보입력, 6-승인

3. 계약 단계 : contractList
0)contractNum(계약번호)    1)date(계약일)    2)strat(공사시작)    3)end(공사끝)    4)name(대표자 성명)
5)businessNum(사업자등록번호)    6)corporationNum(법인등록번호)    7)c_contact(업체 연락처)
8)fax(팩스번호)    9)addr(업체 주소)    10)bankName(은행명)    11)accountHolder(예금주명)		
12)accountNum(계좌번호)

4. 착공 단계
5. 준공 단계

### 메모
: 가스 공사에서 작성한 내용은 업체에서 수정할 수 없도록! 확인만 가능