from flask import Flask, url_for, session, render_template, request, redirect, flash
import sqlite3
from os import path

ROOT = path.dirname(path.realpath(__file__))

app = Flask(__name__)
app.secret_key = 'tjdgus12'
management_KEY = 'KOGAS_333K'   # 관리자 암호키

# ------------------------------------------ Page route ------------------------------------------
# 1. 메인페이지
@app.route('/')
def index():
    # 공사리스트 가져오기
    con = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
    cur = con.cursor()
    sql = f"SELECT * FROM constructionList"
    cur.execute(sql)
    list = cur.fetchall()
    list = sorted(list, key=lambda x : x[0], reverse=True)
    return render_template('index.html', login=session.get('logFlag'), constructionList=list)

# 2. 개요
@app.route('/summary')
def summary():
    return render_template('summary.html')

# 3. 공지사항
@app.route('/notice')
def notice():
    return render_template('notice.html')

# 4. 용역현황
@app.route('/serviceStatus')
def serviceStatus():
    return render_template('serviceStatus.html')

# 5. 공사생성
@app.route('/createConstruction')
def createConstruction():
    # 로그인체크
    if 'userName' in session:
        return render_template('createConstruction.html', login=session.get('logFlag'), lightMode = session.get('light'))
    # 로그인 하지 않으면 로그인 페이지로 이동
    else:
        flash("해당 페이지는 관리자 로그인이 필요합니다.")
        return redirect(url_for("login"))

# 6. 관리자 회원가입 & 로그인
@app.route('/login')
def login():
    return render_template('login.html')

# 7. 업체 로그인
@app.route("/pre/<id>")
def pre(id):
    # 관리자 로그인이 되어 있으면 myPage
    if 'userName' in session:
        return render_template('myPage.html', login=session.get('logFlag'), lightMode = session.get('light'))
    # 로그인 하지 않으면 로그인 페이지로 이동
    else:
        return render_template('pre.html')

# 8. 업체 메인 페이지
@app.route('/myPage')
def myPage():
    return render_template('myPage.html')

# 9. 계약 단계
# 개요
@app.route('/contractPhase')
def contractPhase():
    return render_template('contractPhase.html')
# 기본 정보 입력
@app.route('/contractInput')
def contractInput():
    return render_template('contractInput.html')
# 필요 서류 다운 및 업로드
@app.route('/contractTable')
def contractTable():
    return render_template('contractTable.html')
# 계약서
# 1 : 계약 이행 각서
@app.route("/contract1/<id>")
def contract1(id):
    con1 = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
    cur1 = con1.cursor()
    sql1 = f"SELECT * FROM constructionList WHERE managementNum=?"
    cur1.execute(sql1, (id,))
    data_ = cur1.fetchone()
    return render_template('contract1.html', login=session.get('logFlag'), data_=data_, lightMode = session.get('light'))


# 10. 착공 단계
# 개요
@app.route('/startPhase')
def startPhase():
    return render_template('startPhase.html')
# 기본 정보 입력
@app.route('/startPhaseInput')
def startPhaseInput():
    return render_template('startPhaseInput.html')
# 필요 서류 다운 및 업로드
@app.route('/startPhaseTable')
def startPhaseTable():
    return render_template('startPhaseTable.html')
# 계약서

# 11. 준공 단계
# 개요
@app.route('/completionPhase')
def completionPhase():
    return render_template('completionPhase.html')
# 기본 정보 입력
@app.route('/completionInput')
def completionInput():
    return render_template('completionInput.html')
# 필요 서류 다운 및 업로드
@app.route('/completionTable')
def completionTable():
    return render_template('completionTable.html')
# 계약서

# ------------------------------------------ function ------------------------------------------
# 관리자 회원가입 처리
@app.route('/register', methods=['GET', 'POST'])
def register():
    # 폼에서 가져오기 
    if request.method == 'POST':
        _id_ = request.form['registerId']
        _username_ = request.form['registerUsername']
        _password_ = request.form['registerPw']
        _Cpassword_ = request.form['registerCPw']
        _management_KEY_ = request.form['managementKEY']

    elif request.method =='GET':
        _id_ = request.args.get('registerId')
        _username_ = request.args.get('registerUsername')
        _password_ = request.args.get('registerPw')
        _Cpassword_ = request.args.get('registerCPw')
        _management_KEY_ = request.args.get('managementKEY')

    # 양식 확인
    if len(_id_) == 0:
        flash("Please Enter id")
        return redirect(url_for("login"))
    if len(_username_) == 0:
        flash("Please Enter User name")
        return redirect(url_for("login"))
    if len(_password_) == 0:
        flash("Please Enter Password")
        return redirect(url_for("login"))
    if _password_ != _Cpassword_:
        flash("Please confirm your password")
        return redirect(url_for("login"))

    # ID 중복 확인
    con = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
    cur = con.cursor()
    sql = "SELECT userId FROM userList where userId =?"
    cur.execute(sql, (_id_,))
    result = cur.fetchall()
    if result:  # ID 중복인 경우
        flash("User id already in use.\nPlease enter another name.")
        return redirect(url_for("login"))

    # 관리자키 확인
    elif management_KEY != _management_KEY_:
        flash("관리자 키를 확인해주세요.")
        return redirect(url_for("login"))

    # 가입 성공
    else:
        # DB에 회원가입 정보 삽입
        sql = """
            INSERT INTO userList(userId, userName, userPassword)
            values(?,?,?)
        """
        cur.execute(sql, (_id_,_username_,_password_,))
        con.commit()
        flash("Membership successful! Please login")
        return redirect(url_for("login"))

# 2. 관리자 로그인 처리
@app.route('/login_proc', methods=['GET', 'POST'])
def login_proc():
    global loginId
    if request.method == 'POST':
        loginId = request.form['loginId']
        loginPw = request.form['loginPw']

    elif request.method == 'GET':
        loginId = request.args.get('loginId')
        loginPw = request.args.get('loginPw')

    if len(loginId) == 0:
        flash("Please Enter id")
        return redirect(url_for("login"))
    elif len(loginPw) == 0:
        flash("Please Enter Password")
        return redirect(url_for("login"))
    else:
        con = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
        cur = con.cursor()
        sql = "SELECT * FROM userList where userId =?"
        cur.execute(sql, (loginId,))
        rows = cur.fetchall()

        for rs in rows:
            # 로그인 성공
            if loginId == rs[1] and loginPw == rs[3]:
                session['userName'] = rs[2]
                session['logFlag'] = True
                return redirect(url_for("index"))
            else:
                flash("Please check your ID or password")
                return redirect(url_for("login"))   # 팝업 추가!

        flash("Please check your ID or password")
        return redirect(url_for("login"))

# 4. 로그아웃 처리
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# 5. 공사 생성 처리
@app.route('/createConstruction_proc', methods=['GET', 'POST'])
def createConstruction_proc():
    # 폼에서 가져오기 
    if request.method == 'POST':
        c1 = request.form['C1']
        c2 = request.form['C2']
        c3 = request.form['C3']
        c4 = request.form['C4']
        c5 = request.form['C5']
        c6 = request.form['C6']
        c7 = request.form['C7']
        c8 = request.form['C8']
        c9 = request.form['C9']
        c10 = request.form['C10']
        c11 = request.form['C11']
    
    # DB에 회원가입 정보 삽입
    sql = """
        INSERT INTO constructionList(managementNum, title, company, c_contact,supervisor,s_position,progress,guaranteeAmount,contractAmount,c_start,c_end)
        values(?,?,?,?,?,?,?,?,?,?,?)
    """
    con = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
    cur = con.cursor()
    cur.execute(sql, (c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,))
    con.commit()
    flash("공사 생성 완료")
    return redirect(url_for("index"))

# 계약서 수정시 DB에 입력 처리
@app.route('/postmethod', methods = ['GET', 'POST'])
def postmethod():
    if request.method == 'POST':
        jsdata = request.form['javascript_data']

    elif request.method == 'GET':
        jsdata = request.args.get('javascript_data')
    print(jsdata)
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)

# 메인에서 로그인 체크하는 부분
# if 'userName' in session:
#         # 공사리스트 가져오기
#         con = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
#         cur = con.cursor()
#         sql = f"SELECT * FROM constructionList"
#         cur.execute(sql)
#         list = cur.fetchall()
#         list = sorted(list, key=lambda x : x[0], reverse=True)
#         return render_template('index.html', login=session.get('logFlag'), constructionList=list, lightMode = session.get('light'))

#     # 로그인 하지 않으면 로그인 페이지로 이동
#     else:
#         flash("해당 페이지는 관리자 로그인이 필요합니다.")
#         return redirect(url_for("login"))


# # 사이드바 테마 변경 처리
# @app.route('/layout-sidenav-light')
# def light():
#     if 'light' in session:
#         if session['light'] == True:
#             session['light'] = False
#         else:
#             session['light'] = True
#     else:
#         session['light'] = True
#     return redirect(url_for("index"))