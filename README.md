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
14. 파일 업로드 로직(리펙토링 필요)
15. 승인 요청 관리 페이지
16. 전체 리스트를 승인 관리 페이지에서 확인 -> 승인 후 승인완료 비활성 버튼으로 변경
17. 파일 업로드시 DB의 progress 단계 업데이트
18. 7개의 양식 자동 완성(변수부터 배치하기)
19. 이메일로 승인 요청 보내기

### < 현재 진행중인 작업 >

### < 해야할 작업 >
1. 하자보증금율 등 드랍박스로 수정하고 디폴트는 10%, 직접입력도 넣기
2. 업체 QR로그인

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
0)contractNum(계약번호)    1)title(공사명)     2)department(사업장)    3)company(업체명) 
4)supervisor(공사감독명)   5)s_contact(감독 연락처)
6)contractAmount(계약금액) 7)deposit_rate(계약보증금율)    8)fault_rate(하자보증금율) 
9)progress(진행관리)       10)s_position(감독직위)         11)s_email(감독메일)

// progress 단계
0-계약준비 : 가스공사에서 신규생성

1-계약 정보 입력 완료(0->1)<br>
2-계약 승인 완료 : 가스공사에서 계약 서류 확인 후 승인(1->2)
3-계약 서류 업로드 완료(2->3) +)착공 정보 입력 가능(메뉴 활성화)

4-착공 정보 입력 완료(3->4)
5-착공 승인 완료 : 가스공사에서 착공 서류 확인 및 승인(4->5)
6-착공 서류 업로드 완료(5->6) +)준공 정보 입력 가능(메뉴 활성화)

7-준공 정보 입력 완료(6->7)
8-준공 승인 완료 : 가스공사에서 착공 서류 확인 및 승인(7->8)
9-준공 서류 업로드 완료(8->9)

3. 계약 단계 : contractList
0)contractNum(계약번호)    1)date(계약일)    2)strat(공사시작)    3)end(공사끝)    4)name(대표자 성명)
5)businessNum(사업자등록번호)    6)corporationNum(법인등록번호)    7)c_contact(업체 연락처)
8)fax(팩스번호)    9)addr(업체 주소)    10)bankName(은행명)    11)accountHolder(예금주명)		
12)accountNum(계좌번호)    13)Upload1 14)Upload2  15)Upload3  16)Upload4  17)Upload5  18)Upload6  17)Upload7

4. 착공 단계
5. 준공 단계

### 메모
: 가스 공사에서 작성한 내용은 업체에서 수정할 수 없도록! 확인만 가능
<!-- redirect version
            <form action="{{url_for('fileupload', id ='contract1')}}" method = "POST" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit">
          </form> -->
