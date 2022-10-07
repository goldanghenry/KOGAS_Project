from flask import Flask, url_for, session, render_template, request, redirect, flash, jsonify
import sqlite3
from os import path
import os
from werkzeug.utils import secure_filename

ROOT = path.dirname(path.realpath(__file__))

app = Flask(__name__)
app.secret_key = 'tjdgus12'
management_KEY = 'KOGAS_333K'   # 관리자 암호키

UPLOAD_FOLDER = 'static/contract_dir'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
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
    return render_template('index.html', login=session.get('logFlag'), constructionList=list)

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
        k_data = [ [] for i in range(4)]
        for i in range(4):
            sql = f"SELECT * FROM constructionList WHERE progress=?"
            cur.execute(sql, (i,))
            k_data[i] = cur.fetchall()
        return render_template('serviceStatus.html', login=session.get('logFlag'), k_data0=k_data[0],k_data1=k_data[1],k_data2=k_data[2],k_data3=k_data[3])
    # 로그인 하지 않으면 로그인 페이지로 이동
    else:
        flash("해당 페이지는 관리자 로그인이 필요합니다.")
        return redirect(url_for("login"))

# 관리자 승인 페이지 -> 승인 버튼 처리
@app.route('/approval_proc/<id>')
def approval_proc(id):
    con = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
    cur = con.cursor()
    sql = "UPDATE constructionList SET progress=? WHERE contractNum=?"
    flash(f"계약 승인 완료!")
    cur.execute(sql, (2, id,))
    con.commit()
    return redirect(url_for("serviceStatus"))

# 7. 업체 로그인
@app.route("/goto/<id>")
def goto(id):
    # 관리자 로그인이 되어 있으면 myPage로 이동
    if 'userName' in session:
        # 세션에 contractNum 추가
        session['contractNum'] = id
        return redirect(url_for("contractTable") )
    
    # 관리자 로그인이 되어있지 않으면 업체 로그인 페이지로 이동
    else:
        session['contractNum'] = id
        return render_template('pre.html')

# 5. 공사생성
@app.route('/createConstruction')
def createConstruction():
    # 로그인체크
    if 'userName' in session:
        return render_template('createConstruction.html', login=session.get('logFlag'))
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
    # 관리자 로그인이 되어 있으면 myPage로 이동
    if 'userName' in session:
        # 세션에 contractNum 추가
        session['contractNum'] = id
        return redirect(url_for("myPage"))
    
    # 관리자 로그인이 되어있지 않으면 업체 로그인 페이지로 이동
    else:
        session['contractNum'] = id
        return render_template('pre.html')

# 8. 업체 메인 페이지
@app.route('/myPage')
def myPage():
    # 관리자 로그인 또는 업체 로그인 확인
    if 'userName' in session or session.get('logFlag_b'):
        # DB에서 현재 상태 출력
        con1 = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
        cur1 = con1.cursor()
        sql1 = f"SELECT * FROM constructionList WHERE contractNum=?"
        cur1.execute(sql1, (session.get('contractNum'),))
        data_ = cur1.fetchone()
        session['progress'] = data_[9]
        return render_template('myPage.html', login=session.get('logFlag'), data=data_, progress = session.get('progress'))
    else:
        flash("업체 로그인이 필요합니다")
        return render_template('pre.html')
# 9. 계약 단계
# 개요
@app.route('/contractPhase')
def contractPhase():
    if 'userName' in session or session.get('logFlag_b'):
        return render_template('contractPhase.html', login=session.get('logFlag'), progress = session.get('progress'))
    else:
        flash("업체 로그인이 필요합니다")
        return redirect(url_for("pre"))
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

        sql = "SELECT * FROM contractList WHERE contractNum=?"
        cur.execute(sql, (contractNum,))
        c_data = cur.fetchone()
        # DB에서 현재 상태 출력
        if c_data and k_data[9] >2:
            flash('계약 정보를 수정하면, 가스공사에 변경 승인을 요청합니다.')
        return render_template('contractInput.html', login=session.get('logFlag'), c_data=c_data, k_data=k_data, progress = session.get('progress') )
    else:
        flash("업체 로그인이 필요합니다")
        return redirect(url_for("pre"))
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
        c_data = cur.fetchall()

        # 이미 있다면 update
        if c_data:
            sql = "SELECT * FROM constructionList where contractNum =?"
            cur.execute(sql, (contract_data,))
            k_data = cur.fetchall()

            # 승인 대기 상태(2) -> 업로드 완료시 3으로 변경
            if k_data[0][9]==2 and c_data[0][13] !='#' and c_data[0][14] !='#' and c_data[0][15] !='#' and c_data[0][16] !='#' and c_data[0][17] !='#':
                sql = "UPDATE constructionList SET progress=? WHERE contractNum=?"
                cur.execute(sql, (3, contract_data,))
                con.commit()
                session['progress'] = 3
            else: 
                session['progress'] = k_data[0][9]
            
            return render_template('contractTable.html',login=session.get('logFlag'), progress = session.get('progress'), c_data=c_data, k_data=k_data)
        elif 'userName' in session:
            sql = "SELECT * FROM constructionList where contractNum =?"
            cur.execute(sql, (contract_data,))
            k_data = cur.fetchall()
            flash("주의!! 업체 기본정보 입력전입니다!")
            return render_template('contractTable.html',login=session.get('logFlag'), progress = session.get('progress'), c_data=c_data, k_data=k_data, data=k_data)
        else:
            flash("계약단계의 업체 기본정보를 먼저 입력해주세요!")
            return redirect(url_for("contractInput"))

    else:
        flash("업체 로그인이 필요합니다")
        return redirect(url_for(f"pre/{contract_data}"))
# 계약서
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
        data1 = str(format(int(k_data[6] * k_data[7]),',d'))+'원'
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

# 10. 착공 단계
# 개요
@app.route('/startPhase')
def startPhase():
    if 'userName' in session or session.get('logFlag_b'):
        return render_template('startPhase.html',login=session.get('logFlag'), progress = session.get('progress'))
    else:
        flash("업체 로그인이 필요합니다")
        return redirect(url_for("pre"))
# 기본 정보 입력
@app.route('/startPhaseInput')
def startPhaseInput():
    if 'userName' in session or session.get('logFlag_b'):
        return render_template('startPhaseInput.html',login=session.get('logFlag'), progress = session.get('progress'))
    else:
        flash("업체 로그인이 필요합니다")
        return redirect(url_for("pre"))
# 필요 서류 다운 및 업로드
@app.route('/startPhaseTable')
def startPhaseTable():
    if 'userName' in session or session.get('logFlag_b'):
        return render_template('startPhaseTable.html',login=session.get('logFlag'), progress = session.get('progress'))
    else:
        flash("업체 로그인이 필요합니다")
        return redirect(url_for("pre"))
# 계약서

# 11. 준공 단계
# 개요
@app.route('/completionPhase')
def completionPhase():
    if 'userName' in session or session.get('logFlag_b'):
        return render_template('completionPhase.html',login=session.get('logFlag'), progress = session.get('progress'))
    else:
        flash("업체 로그인이 필요합니다")
        return redirect(url_for("pre"))
# 기본 정보 입력
@app.route('/completionInput')
def completionInput():
    if 'userName' in session or session.get('logFlag_b'):
        return render_template('completionInput.html',login=session.get('logFlag'), progress = session.get('progress'))
    else:
        flash("업체 로그인이 필요합니다")
        return redirect(url_for("pre"))
# 필요 서류 다운 및 업로드
@app.route('/completionTable')
def completionTable():
    if 'userName' in session or session.get('logFlag_b'):
        return render_template('completionTable.html',login=session.get('logFlag'), progress = session.get('progress'))
    else:
        flash("업체 로그인이 필요합니다")
        return redirect(url_for("pre"))
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
        c0 = request.form['C0']
        c1 = request.form['C1']
        c2 = request.form['C2']
        c3 = request.form['C3']
        c4 = request.form['C4']
        c5 = request.form['C5']
        c6 = request.form['C6']
        c7 = request.form['C7']
        c8 = request.form['C8']
        
    # DB에 발주기관 자료 입력
    sql = """
        INSERT INTO constructionList(contractNum, title, department, company,supervisor,s_contact,contractAmount,deposit_rate,fault_rate,progress)
        values(?,?,?,?,?,?,?,?,?,?)
    """
    con = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
    cur = con.cursor()
    cur.execute(sql, (c0,c1,c2,c3,c4,c5,c6,c7,c8,0,))
    con.commit()
    flash("공사 생성 완료")
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
        d5 = request.form['d5']
        d6 = request.form['d6']
        d7 = request.form['d7']
        d8 = request.form['d8']
        d9 = request.form['d9']
        d10 = request.form['d10']
        d11 = request.form['d11']
        d12 = request.form['d12']

    contract_data = session.get('contractNum')
    con = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
    cur = con.cursor()
    sql = "SELECT contractNum FROM contractList where contractNum =?"
    cur.execute(sql, (contract_data,))
    result = cur.fetchall()
    # 이미 있다면 update
    if result:
        sql = """
            UPDATE contractList SET date=?,start=?,end=?,name=?,businessNum=?,corporationNum=?,c_contact=?,fax=?,addr=?,bankName=?,accountHolder=?,accountNum=? WHERE contractNum=?
        """
        cur.execute(sql, (d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12,contract_data,))
        con.commit()
        sql = "UPDATE constructionList SET progress=? WHERE contractNum=?"
        flash("계약 단계 정보 수정 완료\n가스 공사에 승인을 요청합니다.")
        cur.execute(sql, (1, contract_data,))
        con.commit()
        return redirect(url_for("contractPhase"))

    else:
        # 없다면 insert
        sql = """
            INSERT INTO contractList(contractNum, date, start, end, name, businessNum,corporationNum,c_contact,fax,addr,bankName,accountHolder,accountNum )
            values(?,?,?,?,?, ?,?,?,?,?, ?,?,?)
        """
        cur.execute(sql, (contract_data,d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12,))
        con.commit()

        # pregress update
        sql = "UPDATE constructionList SET progress=? WHERE contractNum=?"
        cur.execute(sql, (1, contract_data,))
        con.commit()
        flash("계약 단계 정보 입력 완료\n가스 공사에 승인을 요청합니다.")
    return redirect(url_for("contractPhase"))


# 7. 계약서 수정시 DB에 입력 처리
@app.route('/postmethod', methods = ['POST','GET'])
def postmethod():
    if request.method == 'POST':
        c2 = request.form['javascript_data']
        c3 = request.form['javascript_data1']
        print('Post',c2,c3)
    elif request.method == 'GET':
        c2 = request.args.get('javascript_data')
        c3 = request.args.get('javascript_data1')
        print('get',c2,c3)
    return redirect(url_for("contract1"))

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