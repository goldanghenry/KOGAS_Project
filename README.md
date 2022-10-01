# KOGAS_Project
KOGAS_Project
--------------------------------------------------------------------------------------------<br>
< 현재 진행중인 작업>
- 페이지 생성 및 링크 작업
- 업체 비밀번호 확인 로직
--------------------------------------------------------------------------------------------<br>
< 오리엔테이션 >
- 많이 만들기 보다는 기대효과적인 측면에서 방향을 설정해서 개발. 완성도가 높으면 수의계약도 가능

< 컨설팅 방향 >
- 실제 운영할 때 문서를 현행화 하는 방식
+ 실제 운영할 때 문서들이 현행화를 어떻게? 양식이 변경되는 경우 어떻게 유지보수를 할 지.
+ 피드백이 현행화가 될 수 있는지.

< 문서 >
* 공통
1. 메인페이지 : index.html
2. 개요 : summary.html
3. 공지사항 : notice.html
4. 용역 현황 : serviceStatus.html
5. 공사 리스트 생성 페이지 : createConstruction.html
6. 관리자용 로그인&회원가입 페이지 : login.html

* 업체
1. 업체 비밀번호 확인 : pre.html
  - index.html -> pre/<계약번호> -> myPage.html
2. 업체 홈(현황 한 눈에 보기) : myPage.html

3. 계약 단계 개요 : contractPhase.html
- 기본 정보 입력 : contractInput.html
- 필요 서류 다운로드 및 업로드 : contractDownload.html
	- 해당 서류 페이지는 contract1 부터 시작

4. 착공 단계 개요 : startPhase.html
- 기본 정보 입력 : startPhaseInput.html
- 필요 서류 다운로드 및 업로드 : startPhaseDownload.html
	- 해당 서류 페이지는 start1 부터 시작

5. 준공 단계 개요 : completionPhase.html
- 기본 정보 입력 : completionInput.html
- 필요 서류 다운로드 및 업로드 : completionDownload.html
	- 해당 서류 페이지는 completion1 부터 시작