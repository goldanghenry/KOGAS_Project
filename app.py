from flask import Flask, url_for, session, render_template, request, redirect, flash, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv
import sqlite3
from os import path
import os
from werkzeug.utils import secure_filename
from datetime import datetime as dt

load_dotenv()
ROOT = path.dirname(path.realpath(__file__))
app = Flask(__name__)
GOOGLE_GMAIL_ADDR = os.getenv("GOOGLE_GMAIL_ADDR")
GOOGLE_GMAIL_PW =os.getenv("GOOGLE_GMAIL_PW")
APP_SECRET_KEY = os.getenv("APP_SECRET_KEY")
MANAGEMENT_KEY = os.getenv("MANAGEMENT_KEY")

app.secret_key = APP_SECRET_KEY
management_KEY = MANAGEMENT_KEY

UPLOAD_FOLDER = 'static/contract_dir'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = GOOGLE_GMAIL_ADDR
app.config["MAIL_PASSWORD"] = GOOGLE_GMAIL_PW
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
mail = Mail(app)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

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
    session['logFlag_b'] = False
    session['contractNum'] = False
    return render_template('index.html',supervisor=session.get('supervisor'), login=session.get('logFlag'), constructionList=list)

# 2. 개요
@app.route('/summary')
def summary():
    return render_template('summary.html')

# 3. 공지사항
@app.route('/notice')
def notice():
    return render_template('notice.html')

# 4. 관리자 승인 페이지
@app.route('/serviceStatus')
def serviceStatus():
    # 로그인체크
    if 'userName' in session:
        # DB에서 k_data 가져오기
        con = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
        cur = con.cursor()
        userName = session.get('userName')
        sql = f"SELECT * FROM constructionList WHERE start_date=? AND (progress!=1 or progress!=3)"
        cur.execute(sql, (userName,))
        A_data = cur.fetchall()

        sql = f"SELECT * FROM constructionList WHERE start_date=? AND progress=1 or progress=3"
        cur.execute(sql, (userName,))
        R_data = cur.fetchall()
        
        process = ['신규 생성','계약 정보 승인 대기','계약 서류 업로드','계약 서류 승인 대기','착공 서류 업로드','착공 서류 승인 대기','준공 정보 입력','준공 정보 승인 대기','준공 서류 업로드','준공 승인 완료']

        return render_template('serviceStatus.html',supervisor=session.get('supervisor'), login=session.get('logFlag'), A_data=A_data, R_data=R_data,process=process)
    # 로그인 하지 않으면 로그인 페이지로 이동
    else:
        flash("해당 페이지는 관리자 로그인이 필요합니다.")
        return redirect(url_for("login"))

# 관리자 승인 페이지 -> 승인 버튼 처리
@app.route('/approval_proc/<id>')
def approval_proc(id):
    print(id)
    con = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
    cur = con.cursor()
    
    sql = "SELECT progress FROM constructionList WHERE contractNum=? "
    cur.execute(sql, (id,))
    progress = cur.fetchone()

    if progress[0] == 1:
        sql = "UPDATE constructionList SET progress=? WHERE contractNum=?"
        cur.execute(sql, (2, id,))
        flash(f"계약 정보 승인 완료!")
    elif progress[0] == 3:
        sql = "UPDATE constructionList SET progress=? WHERE contractNum=?"
        cur.execute(sql, (4, id,))
        flash(f"서류 업로드 승인 완료!")
    con.commit()

    return redirect(url_for("serviceStatus"))

# contractInput으로 이동
@app.route("/goto/<id>")
def goto(id):
    # 관리자 로그인이 되어 있으면 myPage로 이동
    if 'userName' in session:
        # 세션에 contractNum 추가
        session['contractNum'] = id
        return redirect(url_for("contractInput") )
    
    # 관리자 로그인이 되어있지 않으면 업체 로그인 페이지로 이동
    else:
        session['contractNum'] = id
        return render_template('pre.html')

# contractTable로 이동
@app.route("/go1/<id>")
def go1(id):
    # 관리자 로그인이 되어 있으면 myPage로 이동
    if 'userName' in session:
        # 세션에 contractNum 추가
        session['contractNum'] = id
        return redirect(url_for("contractTable") )
    
    # 관리자 로그인이 되어있지 않으면 업체 로그인 페이지로 이동
    else:
        session['contractNum'] = id
        return render_template('pre.html')

# myPage로 이동
@app.route("/go/<id>")
def go(id):
    # 관리자 로그인이 되어 있으면 myPage로 이동
    if 'userName' in session:
        # 세션에 contractNum 추가
        session['contractNum'] = id
        return redirect(url_for("myPage") )
    
    # 관리자 로그인이 되어있지 않으면 업체 로그인 페이지로 이동
    else:
        session['contractNum'] = id
        return render_template('pre.html')

# 5. 공사생성
@app.route('/createConstruction')
def createConstruction():
    # 로그인체크
    if 'userName' in session:
        return render_template('createConstruction.html', login=session.get('logFlag'), supervisor=session.get('supervisor'))
    # 로그인 하지 않으면 로그인 페이지로 이동
    else:
        flash("해당 페이지는 관리자 로그인이 필요합니다.")
        return redirect(url_for("login"))

# 6. 관리자 회원가입 & 로그인
@app.route('/login')
def login():
    return render_template('login.html')

@app.route("/pr/<id>")
def pr(id):
    # 관리자 로그인이 되어 있으면 myPage로 이동
    if 'userName' in session:
        # 세션에 contractNum 추가
        session['contractNum'] = id
        return redirect(url_for("myPage"))
    
    # 관리자 로그인이 되어있지 않으면 업체 로그인 페이지로 이동
    else:
        session['contractNum'] = id
        return redirect(url_for("pre"))


# 7. 업체 로그인
@app.route("/pre")
def pre():
    return render_template('pre.html')

# 8. 업체 메인 페이지
@app.route('/myPage')
def myPage():
    # 관리자 로그인 또는 업체 로그인 확인
    if 'userName' in session or session.get('logFlag_b'):
        # DB에서 현재 상태 출력
        con = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
        cur = con.cursor()
        sql = f"SELECT * FROM constructionList WHERE contractNum=?"
        cur.execute(sql, (session.get('contractNum'),))
        k_data = cur.fetchone()
        session['progress'] = k_data[9]
        contractNum = session.get('contractNum')
        sql = "SELECT * FROM contractList WHERE contractNum=?"
        cur.execute(sql, (contractNum,))
        c_data = cur.fetchone()
        data1 = str(format(int(k_data[6]),',d'))+'원'        
        return render_template('myPage.html', login=session.get('logFlag'), k_data=k_data, c_data=c_data,data1=data1, progress = session.get('progress'), supervisor=session.get('supervisor'))
    else:
        flash("업체 로그인이 필요합니다")
        return render_template('pre.html')
# 9. 계약 단계
# 기본 정보 입력
@app.route('/contractInput')
def contractInput():
    # 관리자 로그인 또는 업체 로그인 확인
    if 'userName' in session or session.get('logFlag_b'):
        contractNum = session.get('contractNum')
        con = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
        cur = con.cursor()
        sql1 = f"SELECT * FROM constructionList WHERE contractNum=?"
        cur.execute(sql1, (contractNum,))
        k_data= cur.fetchone()
        session['progress'] = k_data[9]
        sql = "SELECT * FROM contractList WHERE contractNum=?"
        cur.execute(sql, (contractNum,))
        c_data = cur.fetchone()

        data1 = str(format(int(k_data[6]),',d'))+'원'

        if c_data:
            session['update_input'] = True
        else:
            session['update_input'] = False

        # DB에서 현재 상태 출력
        if c_data and k_data[9] >2:
            flash('계약 정보를 수정하면, 가스공사에 변경 승인을 재요청합니다.')
        return render_template('contractInput.html', update =session.get('update_input'), login=session.get('logFlag'),data1=data1, c_data=c_data, k_data=k_data, progress = session.get('progress'), supervisor=session.get('supervisor') )
    else:
        flash("업체 로그인이 필요합니다")
        return redirect(url_for("pre"))

@app.route('/forbidden')
def forbidden():
    flash('감독 승인 전입니다.')
    return redirect(url_for("myPage"))
        
# 필요 서류 다운 및 업로드
@app.route('/contractTable')
def contractTable():
    contract_data = session.get('contractNum')
    if 'userName' in session or session.get('logFlag_b'):
        # 기본 정보를 입력했는지 체크
        con = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
        cur = con.cursor()
        sql = "SELECT * FROM contractList where contractNum =?"
        cur.execute(sql, (contract_data,))
        c_data = cur.fetchone()

        # 이미 있다면 update
        if c_data:
            sql = "SELECT * FROM constructionList where contractNum =?"
            cur.execute(sql, (contract_data,))
            k_data = cur.fetchone()

            # 승인 대기 상태(3) -> 업로드 완료시 3으로 변경
            if k_data[9]==2 and c_data[13] !='#' and c_data[14] !='#' and c_data[15] !='#' and c_data[16] !='#' and c_data[17] !='#' and c_data[18] !='#' and c_data[19] !='#' and c_data[20] !='#':
                sql = "UPDATE constructionList SET progress=? WHERE contractNum=?"
                cur.execute(sql, (3, contract_data,))
                con.commit()
                session['progress'] = 3
                msg = Message(f'{k_data[1]} 공사건 계약서류 업로드 승인 요청', sender='#@gmail.com', recipients=[k_data[11]])
                msg.body = f"""
                {k_data[1]} 공사건의 계약서류가 업로드 되었습니다.
                서류를 검토 후 승인 처리해주세요.
                링크 : https://kogasonestop.pythonanywhere.com/serviceStatus
                """
                mail.send(msg)
                flash("공사 감독관에 계약 서류 승인을 요청합니다.")
            else:
                session['progress'] = k_data[9]
            return render_template('contractTable.html',login=session.get('logFlag'), progress = session.get('progress'), c_data=c_data, k_data=k_data,supervisor=session.get('supervisor'))
        
        elif 'userName' in session:
            flash("업체 계약 정보 승인 전입니다!")
            return redirect(url_for("myPage"))
        else:
            flash("계약단계의 기본정보를 먼저 입력해주세요!")
            return redirect(url_for("contractInput"))

    else:
        flash("업체 로그인이 필요합니다")
        return redirect(url_for(f"pre/{contract_data}"))

@app.route("/contractTable_proc")
def contractTable_proc():
    flash("저장완료!")
    return redirect(url_for("contractTable"))

# 계약서
# 1: 간이공사지시서
@app.route("/contract1")
def contract1():
    contract_data = session.get('contractNum')
    # 업체 입력 데이터 가져오기
    con = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
    cur = con.cursor()
    sql = "SELECT * FROM contractList WHERE contractNum=?"
    cur.execute(sql, (contract_data,))
    c_data = cur.fetchone()

    if c_data:
        # 가스공사 데이터 가져오기
        sql = "SELECT * FROM constructionList WHERE contractNum=?"
        cur.execute(sql, (contract_data,))
        k_data = cur.fetchone()
        # 업체 1금액
        data1 = str(format(k_data[6],',d'))+'원'
        # 업체 2금액
        if k_data[19] == 0:
            data2 = '-'    
        else:
            data2 = str(format(k_data[19],',d'))+'원'
        # 업체 3금액
        if k_data[21] == 0:
            data3 = '-'    
        else:
            data3 = str(format(k_data[21],',d'))+'원'
        return render_template('contract1.html', login=session.get('logFlag'), k_data=k_data, c_data=c_data, data1= data1, data2=data2, data3=data3)
    else:
        flash("계약단계의 업체 기본정보 입력전입니다.")
        return redirect(url_for("contractInput"))
# 2: 계약이행보증금 지급확약서
@app.route("/contract2")
def contract2():
    contract_data = session.get('contractNum')
    # 업체 입력 데이터 가져오기
    con = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
    cur = con.cursor()
    sql = "SELECT * FROM contractList WHERE contractNum=?"
    cur.execute(sql, (contract_data,))
    c_data = cur.fetchone()

    if c_data:
        # 가스공사 데이터 가져오기
        sql = "SELECT * FROM constructionList WHERE contractNum=?"
        cur.execute(sql, (contract_data,))
        k_data = cur.fetchone()
        data1 = str(format(int(k_data[6] * (k_data[7]/100)),',d'))+'원'
        data2 = str(format(k_data[6],',d'))+'원'
        return render_template('contract2.html', login=session.get('logFlag'), k_data=k_data, c_data=c_data, data1= data1, data2=data2)
    else:
        flash("계약단계의 업체 기본정보 입력전입니다.")
        return redirect(url_for("contractInput"))

# 3: 하자보증이행각서
@app.route("/contract3")
def contract3():
    contract_data = session.get('contractNum')
    # 업체 입력 데이터 가져오기
    con = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
    cur = con.cursor()
    sql = "SELECT * FROM contractList WHERE contractNum=?"
    cur.execute(sql, (contract_data,))
    c_data = cur.fetchone()

    if c_data:
        # 가스공사 데이터 가져오기
        sql = "SELECT * FROM constructionList WHERE contractNum=?"
        cur.execute(sql, (contract_data,))
        k_data = cur.fetchone()
        data2 = str(format(k_data[6],',d'))+'원'
        t = c_data[1]
        data3 = t[:4]+ '년 '+t[5:7]+'월 '+t[8:]+'일'
        return render_template('contract3.html', login=session.get('logFlag'), k_data=k_data, c_data=c_data, data3= data3, data2=data2)
    else:
        flash("계약단계의 업체 기본정보 입력전입니다.")
        return redirect(url_for("contractInput"))

# 4: 사용인감계
@app.route("/contract4")
def contract4():
    contract_data = session.get('contractNum')
    # 업체 입력 데이터 가져오기
    con = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
    cur = con.cursor()
    sql = "SELECT * FROM contractList WHERE contractNum=?"
    cur.execute(sql, (contract_data,))
    c_data = cur.fetchone()

    if c_data:
        # 가스공사 데이터 가져오기
        sql = "SELECT * FROM constructionList WHERE contractNum=?"
        cur.execute(sql, (contract_data,))
        k_data = cur.fetchone()
        t = c_data[1]
        data3 = t[:4]+ '년 '+t[5:7]+'월 '+t[8:]+'일'
        return render_template('contract4.html', login=session.get('logFlag'), k_data=k_data, c_data=c_data, data3= data3)
    else:
        flash("계약단계의 업체 기본정보 입력전입니다.")
        return redirect(url_for("contractInput"))

# 5: 청렴계약이행서약서(업체용)
@app.route("/contract5")
def contract5():
    contract_data = session.get('contractNum')
    # 업체 입력 데이터 가져오기
    con = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
    cur = con.cursor()
    sql = "SELECT * FROM contractList WHERE contractNum=?"
    cur.execute(sql, (contract_data,))
    c_data = cur.fetchone()

    if c_data:
        t = c_data[1]
        data3 = t[:4]+ '년 '+t[5:7]+'월 '+t[8:]+'일'
        return render_template('contract5.html', login=session.get('logFlag'), c_data=c_data, data3= data3)
    else:
        flash("계약단계의 업체 기본정보 입력전입니다.")
        return redirect(url_for("contractInput"))

# 6: 청렴계약이행서약서(교부용)
@app.route("/contract6")
def contract6():
    contract_data = session.get('contractNum')
    # 업체 입력 데이터 가져오기
    con = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
    cur = con.cursor()
    sql = "SELECT * FROM contractList WHERE contractNum=?"
    cur.execute(sql, (contract_data,))
    c_data = cur.fetchone()

    if c_data:
        sql = "SELECT * FROM constructionList WHERE contractNum=?"
        cur.execute(sql, (contract_data,))
        k_data = cur.fetchone()
        t = c_data[1]
        data3 = t[:4]+ '년 '+t[5:7]+'월 '+t[8:]+'일'
        return render_template('contract6.html', login=session.get('logFlag'),data3= data3, k_data=k_data)
    else:
        flash("계약단계의 업체 기본정보 입력전입니다.")
        return redirect(url_for("contractInput"))

# 7: 청렴계약이행서약서(직원용)
@app.route("/contract7")
def contract7():
    contract_data = session.get('contractNum')
    # 업체 입력 데이터 가져오기
    con = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
    cur = con.cursor()
    sql = "SELECT * FROM contractList WHERE contractNum=?"
    cur.execute(sql, (contract_data,))
    c_data = cur.fetchone()

    if c_data:
        sql = "SELECT * FROM constructionList WHERE contractNum=?"
        cur.execute(sql, (contract_data,))
        k_data = cur.fetchone()
        t = c_data[1]
        data3 = t[:4]+ '년 '+t[5:7]+'월 '+t[8:]+'일'
        return render_template('contract7.html', login=session.get('logFlag'),data3= data3, k_data=k_data)
    else:
        flash("계약단계의 업체 기본정보 입력전입니다.")
        return redirect(url_for("contractInput"))

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

                sql = "SELECT supervisor FROM constructionList where start_date=?"
                cur.execute(sql, (loginId,))
                supervisor = cur.fetchone()
                session['supervisor'] = supervisor[0]+"님"
                session['userName'] = loginId
                session['logFlag'] = True
                return redirect(url_for("index"))
            else:
                flash("Please check your ID or password")
                return redirect(url_for("login"))   # 팝업 추가!

        flash("Please check your ID or password")
        return redirect(url_for("login"))

# 4. 로그아웃 처리
@app.route('/logout',methods=["POST"])
def logout():
    if request.method =="POST":
        userInput = request.form.get("userInput")
        if userInput=="True":
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
        c10 = request.form['C10']
        c11 = request.form['C11']
        c12 = request.form['C12']   # 공사 구분
        c13 = request.form['C13']
        # c14 = request.form['C14']
        # c15 = request.form['C15']
        # c16 = request.form['C16']
        c17 = request.form['C17']
        c18 = request.form['C18']
        c19 = request.form['C19']
        c20 = request.form['C20']
        c21 = request.form['C21']
        
        # 관리자 추가
        c14=session.get('userName')
        
        # DB 연결
        con = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
        cur = con.cursor()
        sql = "SELECT contractNum FROM constructionList"
        cur.execute(sql)
        result = cur.fetchall() 
        
        # 관리 번호 생성
        today = dt.today()      # 오늘 날짜
        num = len(result)+1
        num_str = str(num)
        num_str = num_str.zfill(4)    
        c0 = str(today.year)+str(c2)+num_str

        # 사업장 코드 dictionary
        code_dic = {'none':'선택','AZ':'본사','BZ':'가스연구원','CZ':'평택기지본부','HZ':'인천기지본부','RZ':'통영기지본부','SZ':'삼척기지본부','PZ':'제주LNG본부','EZ':'서울지역본부','DZ':'경기지역본부','FZ':'대전충청지역본부','KZ':'대구경북지역본부','IZ':'광주전남지역본부','JZ':'부산경남지역본부','VZ':'강원지역본부','XZ':'전북지역본부','LZ':'인천지역본부','WZ':'중부안전건설단','YZ':'남부안전건설단','ZZ':'당진기지안전건설단'}

    # DB에 발주기관 자료 입력
    sql = """
        INSERT INTO constructionList(contractNum, title, department, company,supervisor,s_contact,contractAmount,deposit_rate,fault_rate,progress,s_position,s_email,class_code,budget_course,start_date,contract_completion,real_completion,summary,company2,company2_amount,company3,company3_amount)
        values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """
    cur.execute(sql, (c0,c1,code_dic[c2],c3,c4,c5,c6,c7,c8,0,c10,c11,c12,c13,c14,'none','none',c17,c18,c19,c20,c21,))
    con.commit()
    flash("생성 완료")
    return redirect(url_for("index"))

# 6. 업체 로그인 처리(계약 번호 확인)
@app.route('/pre_proc', methods=['POST','GET'])
def pre_proc():
    if request.method == 'POST':
        input_data = request.form['d1']
    elif request.method == 'GET':
        input_data = request.args.get('d1')

    contract_data = session.get('contractNum')
    if  contract_data == input_data:
        session['logFlag_b'] = True
        flash("업체 로그인 완료!")
        return redirect(url_for("myPage"))
    else:
        flash("Please check your password")
        return render_template('pre.html')

# 7. 계약 단계 업체 정보 입력 처리
@app.route('/contractInput_proc', methods=['GET', 'POST'])
def contractInput_proc():
    # 폼에서 가져오기
    if request.method == 'POST':
        d1 = request.form['d1']
        d2 = request.form['d2']
        d3 = request.form['d3']
        d4 = request.form['d4']
        d5 = str(request.form['d5'])
        d6 = str(request.form['d6'])
        d7 = str(request.form['d7'])
        d8 = str(request.form['d8'])
        d9 = request.form['d9']
        # d10 = request.form['d10']
        # d11 = request.form['d11']
        # d12 = request.form['d12']

    contract_data = session.get('contractNum')
    con = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
    cur = con.cursor()
    sql = "SELECT contractNum FROM contractList where contractNum =?"
    cur.execute(sql, (contract_data,))
    result = cur.fetchall()
    login1 = session.get('logFlag')

    # 이미 있다면 update
    if result:
        sql = """
            UPDATE contractList SET date=?,start=?,end=?,name=?,businessNum=?,corporationNum=?,c_contact=?,fax=?,addr=?,bankName=?,accountHolder=?,accountNum=? WHERE contractNum=?
        """
        cur.execute(sql, (d1,d2,d3,d4,d5,d6,d7,d8,d9,'none','none','none',contract_data,))
        con.commit()
        sql = "UPDATE constructionList SET progress=? WHERE contractNum=?"
        cur.execute(sql, (1, contract_data,))
        con.commit()
        flash("계약 단계 정보 수정 완료\n가스 공사에 승인을 요청합니다.")

        sql = "SELECT * FROM constructionList WHERE contractNum=?"
        cur.execute(sql, (contract_data,))
        k_data = cur.fetchone()

        if login1:
            return redirect(url_for("serviceStatus"))
        else:
            # 관리자 이 메일로 승인 요청 메일 전송
            msg = Message(f'{k_data[1]} 공사건 승인 요청', sender='#@gmail.com', recipients=[k_data[11]])
            msg.body = f"""
            {k_data[1]} 계약 단계에 대한 업체 정보가 수정되었습니다.
            서류를 검토 후 승인 처리해주세요.
            링크 : https://kogasonestop.pythonanywhere.com/serviceStatus
            """
            mail.send(msg)
            return redirect(url_for("myPage"))

    else:
        # 없다면 insert
        sql = """
            INSERT INTO contractList(contractNum, date, start, end, name, businessNum,corporationNum,c_contact,fax,addr,bankName,accountHolder,accountNum )
            values(?,?,?,?,?, ?,?,?,?,?, ?,?,?)
        """
        cur.execute(sql, (contract_data,d1,d2,d3,d4,d5,d6,d7,d8,d9,'none','none','none',))
        con.commit()

        # pregress update
        sql = "UPDATE constructionList SET progress=? WHERE contractNum=?"
        cur.execute(sql, (1, contract_data,))
        con.commit()
        flash("계약 단계 정보 입력 완료\n가스 공사에 승인을 요청합니다.")
        
        sql = "SELECT * FROM constructionList WHERE contractNum=?"
        cur.execute(sql, (contract_data,))
        k_data = cur.fetchone()
        
        # 관리자 이 메일로 승인 요청 메일 전송
        msg = Message(f'{k_data[1]} 공사건 승인 요청', sender='#@naver.com', recipients=[k_data[11]])
        msg.body = f"""
        {k_data[1]} 공사건의 계약 단계에 대한 업체 정보 입력이 완료되었습니다.
        서류를 검토 후 승인 처리해주세요.
        링크 : https://kogasonestop.pythonanywhere.com/serviceStatus
        """
        mail.send(msg)
        return redirect(url_for("myPage"))

# 7. 계약서 수정시 DB에 입력 처리
# @app.route('/postmethod', methods = ['POST','GET'])
# def postmethod():
#     if request.method == 'POST':
#         c2 = request.form['javascript_data']
#         c3 = request.form['javascript_data1']
#     elif request.method == 'GET':
#         c2 = request.args.get('javascript_data')
#         c3 = request.args.get('javascript_data1')
#     return redirect(url_for("contract1"))

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('file-upload.html')

@app.route('/python-flask-files-upload', methods=['POST'])
def upload_file():
    if 'files[]' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    contract_data = session.get('contractNum')
    files = request.files.getlist('files[]')
    f_name = request.form['filename']
    errors = {}
    success = False

    for file in files:
        if file and allowed_file(file.filename):
            image_path = f'static/contract_dir/{contract_data}'
            os.makedirs(image_path, exist_ok=True)
            file.save(os.path.join(image_path, file.filename))

            # DB에 file path 저장
            con = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
            cur = con.cursor()
            sql = f"UPDATE contractList SET {f_name}=? WHERE contractNum=?"
            cur.execute(sql, (file.filename, contract_data,))
            con.commit()
            success = True
        else:
            errors['message'] = 'File type is not allowed'

    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 206
        return resp
    if success:
        resp = jsonify({'message' : '파일 업로드 성공'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 400
        return resp

if __name__ == '__main__':
    app.run(debug=True)