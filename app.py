from flask import Flask, url_for, session, render_template, request, redirect, flash
import sqlite3
from os import path

ROOT = path.dirname(path.realpath(__file__))

app = Flask(__name__)
app.secret_key = 'tjdgus12'
management_KEY = 'KOGAS_333K'   # 관리자 암호키

# --------------------- Page route ---------------------
# main page
@app.route('/')
def index():
    # 로그인 검사
    if 'userName' in session:
        # 공사리스트 가져오기
        con = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
        cur = con.cursor()
        sql = f"SELECT * FROM constructionList"
        cur.execute(sql)
        list = cur.fetchall()
        list = sorted(list, key=lambda x : x[0], reverse=True)
        return render_template('index.html', login=session.get('logFlag'), constructionList=list, lightMode = session.get('light'))

    # 로그인 하지 않으면 로그인 페이지로 이동
    else:
        flash("해당 페이지는 관리자 로그인이 필요합니다.")
        return redirect(url_for("login"))

# log-in page
@app.route('/login')
def login():
    return render_template('login.html')

# 공사 생성하기 페이지
@app.route('/createConstruction')
def createConstruction():
    return render_template('createConstruction.html', login=session.get('logFlag'), lightMode = session.get('light'))

# 공사 상세 페이지
@app.route("/go_detail/<id>")
def construction_detail(id):
    con1 = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
    cur1 = con1.cursor()
    sql1 = f"SELECT * FROM constructionList WHERE managementNum=?"
    cur1.execute(sql1, (id,))
    data_ = cur1.fetchone()
    return render_template('contact_doc.html', login=session.get('logFlag'), data_=data_, lightMode = session.get('light'))

# --------------------- function ---------------------
# 로그인
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
            # 아이디 비밀번호 동일
            if loginId == rs[1] and loginPw == rs[3]:
                session['userName'] = rs[2]
                session['logFlag'] = True
                return redirect(url_for("index"))
            else:
                flash("Please check your ID or password")
                return redirect(url_for("login"))   # 팝업 추가!

        flash("Please check your ID or password")
        return redirect(url_for("login"))

# 관리자 회원가입
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

    # 닉네임 중복 확인
    con = sqlite3.connect(path.join(ROOT, 'KOGAS.db'))
    cur = con.cursor()
    sql = "SELECT userId FROM userList where userId =?"
    cur.execute(sql, (_id_,))
    result = cur.fetchall()

    # 닉네임 중복인 경우
    if result:
        flash("User id already in use.\nPlease enter another name.")
        return redirect(url_for("login"))

    # 관리자키 확인
    elif management_KEY != _management_KEY_:
        flash("관리자 키를 확인해주세요.")
        return redirect(url_for("login"))

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

# 공사 생성하기
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

    # elif request.method =='GET':
    #     _id_ = request.args.get('registerId')
    #     _username_ = request.args.get('registerUsername')
    #     _password_ = request.args.get('registerPw')
    #     _Cpassword_ = request.args.get('registerCPw')
    #     _management_KEY_ = request.args.get('managementKEY')

    
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

# 로그아웃 버튼
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# 사이드바 테마
@app.route('/layout-sidenav-light')
def light():
    if 'light' in session:
        if session['light'] == True:
            session['light'] = False
        else:
            session['light'] = True
    else:
        session['light'] = True
    return redirect(url_for("index"))



# @app.route('/bookmarks')
# def bookmarks():
#     # 로그인 검사
#     if 'userName' in session:
#         # 기사 리스트 가져오기
#         userid = session.get('userId')
#         tableName = userid.replace('@','').replace('.','')

#         con = sqlite3.connect(path.join(ROOT, 'Keyword_Statics.db'))
#         cur = con.cursor()
#         sql = f"SELECT * FROM {tableName}"
#         cur.execute(sql)
#         list = cur.fetchall()
#         list = sorted(list, key=lambda x : (x[3], x[4]), reverse=True)
#         return render_template('bookmarks.html', userName=session.get("userName"), login=session.get('logFlag'), articleList=list, lightMode = session.get('light'))
#     # 로그인 하지 않으면 로그인 페이지로 이동
#     else:
#         flash("북마크 페이지는 로그인을 해야 이용할 수 있습니다.")
#         return redirect(url_for("login"))

# @app.route("/favorite1/<int:idx>")
# def favorite1(idx):
#     #클릭한 뉴스 객체 가져오기
#     con = sqlite3.connect(path.join(ROOT, 'Keyword_Statics.db'))
#     cur = con.cursor()
#     sql = "SELECT * FROM ArticleList WHERE idx=?"
#     cur.execute(sql, (idx,))
#     selectedN = cur.fetchall()
#     selectedN = selectedN[0]

#     con = sqlite3.connect(path.join(ROOT, 'Keyword_Statics.db'))
#     cur = con.cursor()
#     userid = session.get('userId')
#     tableName = userid.replace('@','').replace('.','')
#     sql = f"DELETE FROM {tableName} WHERE idx= ?"
#     cur.execute(sql, (selectedN[0],))
#     con.commit()
#     return redirect(url_for("index"))

# @app.route('/charts')
# def charts():
#     # datelist
#     con = sqlite3.connect(path.join(ROOT, 'Keyword_Statics.db'))
#     cur = con.cursor()
#     sql = "SELECT dates FROM Ranked_Tags"
#     cur.execute(sql)
#     dateList = cur.fetchall()
#     dateList = set(dateList)
#     dateList = sorted(dateList, key=lambda x : (x[0]), reverse=True)

#     dList = []
#     for d in dateList:
#         dList.append(d[0][4:8])
#     return render_template('charts.html', dateList=dList, lightMode = session.get('light'))

if __name__ == '__main__':
    app.run(debug=True)