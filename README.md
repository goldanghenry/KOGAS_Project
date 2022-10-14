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
11. 계약 단계 table 생성 및 새 창에서 계약서 띄우기, vertical-align : middle
12. 웹 계약서에서 두개 이상 수정 후 DB 테스트
13. contractInput.html 이미 입력한 정보가 있다면 placeholder나 data-default로 표시하기
14. 파일 업로드(ajax로 비동기 처리) 및 웹에서 미리보기
15. 승인 요청 관리 페이지
16. 전체 리스트를 승인 관리 페이지에서 확인 -> 승인 후 승인완료 비활성 버튼으로 변경
17. 파일 업로드시 DB의 progress 단계 업데이트
18. 7개의 양식 자동 완성(변수부터 배치하기)
19. 이메일로 승인 요청 보내기
20. 공사 생성 - 계약번호 -> 관리번호(년도+사업장코드+순번)
21. 우측 메뉴 수정 및 가스공사 인풋 양식 수정
22. 간이공사지시서 양식 추가
23. 관리자 승인 페이지 -> 자신이 담당하는 공사만 모아서 보여주기
24. 메인화면 우측 상단 로그인 버튼 생성
25. 메인화면 홈 (공지사항, 개요, 공사/용역 리스트)
26. 메인화면 공지사항 / 간이공사 진행리스트 오른쪽 더보기 버튼 생성
27. 관리번호 자동생성 (수정 불가) > 업체 비밀번호로 사용
28. 메인화면 진행 리스트 (구분 - 계약건명 - 사업장) 으로 변경
29. 공사 신규 생성 화면 > 공사 구분 > 계약번호 삭제
30. 공사 신규 생성 화면 > 공사 내용 > 분류기호, 착공일, 실 준공일 삭제
31. 공사 신규 생성 화면 > 공사 내용 > 계약일, 공사기간 추가
32. 공사 신규 생성 화면 > 계약 정보 > 계약 금액을 견적 금액으로 변경하고 표로 표시(간이공사 지시서 표 참고)
33. 공사 신규 생성 후 데이터 수정 기능 필요
34. 관리자 로그인 > 홈 메뉴(공지사항, 개요, 공사/용역 리스트) 동일
35. 관리자 로그인 > 오른쪽 상단 MY PAGE 버튼 생성 > 클릭 시 공사/용역 현황 화면
36. 업체에서 서류 업로드 후 저장 > 승인 요청
37. 현황 한눈에 보기 > 업무 프로세스바 추가
38. 메뉴는 사라지지 않고 클릭 시 팝업창 또는 비활성화 처리
39. 본인이 담당하는 공사/용역만 수정 가능
40. 업체 인풋 창에 계약 정보 추가하기
41. 관리자가 수정할 때는 저장 후 다시 관리자 페이지로 이동
42. 공통 > 헤더 > 헤더 왼쪽 KOGAS로고 추가, 오른쪽 로그인 한 유저 이름
43. 기본정보 > 업체정보 입력 > 일자 -> 달력 선택으로 변경, 전화번호 등록번호 등 -> 숫자만 입력 할 수 있도 록 변경
44. 기본 정보 내역 승인 전 필요 서류 네비게이션 클릭 시 •승인 전입니다. Alert
45. 마이페이지 프로세스 밑에 기본정보, 업체정보 추가
46. 파일 업로드 후 승인 단계 추가

### < 현재 진행중인 작업 >
로그아웃 -> 로그아웃 하시겠습니까?
필요 서류 확인 및 업로드 > PDF 파일 가능 하도록
간이공사 지시서 > 공사 개요 및 시방 > 엔터 인식되도록

### < 해야할 작업 >
1. 업체 QR로그인

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
4. 공사진행 현황 : serviceStatus.html
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
  +) 간이공사지시서는 업로드 -> 출력 확인만 가능

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
1 공사 구분<br>
0)contractNum(계약번호)    1)title(공사명)     2)department(사업장)    3)company(업체명)
2 감독 정보<br>
4)supervisor(공사감독명)   5)s_contact(감독 연락처) 10)s_position(감독직위)  11)s_email(감독메일)
3 공사 내용<br>
12)class_code(분류기호)  13)budget_course(예산 과목)   14)start_date(착공일) 15)contract_completion(계약 준공일)   16)real_completion(실준공일)     17)summary(공사 개요 및 시방)
4 계약 정보<br>
6)contractAmount(계약금액1) 7)deposit_rate(계약보증금율)    8)fault_rate(하자보증금율) 
18)company2(업체명2)  19)company2_amount(업체2계약금액) 20)company3(업체명3) 21)company3_amount(업체3계약금액)

9)progress(진행관리)

3. 계약 단계 : contractList
0)contractNum(계약번호)    1)date(계약일)    2)strat(공사시작)    3)end(공사끝)    4)name(대표자 성명)
5)businessNum(사업자등록번호)    6)corporationNum(법인등록번호)    7)c_contact(업체 연락처)
8)fax(팩스번호)    9)addr(업체 주소)    10)bankName(은행명)    11)accountHolder(예금주명)		
12)accountNum(계좌번호)    13)Upload1 14)Upload2  15)Upload3  16)Upload4  17)Upload5  18)Upload6  17)Upload7

// progress 단계
0-계약준비 : 가스공사에서 신규생성

1-계약 정보 입력 완료(0->1)<br>
2-계약 승인 완료 : 가스공사에서 계약 서류 확인 후 승인(1->2)<br>
3-계약 서류 업로드 완료(2->3) +)착공 정보 입력 가능(메뉴 활성화)<br><br>

4-착공 정보 입력 완료(3->4)<br>
5-착공 승인 완료 : 가스공사에서 착공 서류 확인 및 승인(4->5)<br>
6-착공 서류 업로드 완료(5->6) +)준공 정보 입력 가능(메뉴 활성화)<br><br>

7-준공 정보 입력 완료(6->7)<br>
8-준공 승인 완료 : 가스공사에서 착공 서류 확인 및 승인(7->8)<br>
9-준공 서류 업로드 완료(8->9)<br><br>

4. 착공 단계
5. 준공 단계

### 메모
: 가스 공사에서 작성한 내용은 업체에서 수정할 수 없도록! 확인만 가능