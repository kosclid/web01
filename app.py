from flask import Flask, render_template, request, redirect
import os
import dbconn as db

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/blog')
def blog():
    return render_template('blog.html')



@app.route('/test/<username>')
def test(username):
    print(username)
    return render_template('test_result.html', name = username)



@app.route('/methodin')
def methodin():
    return render_template('inputform.html')

@app.route('/methodout', methods = ['GET', 'POST'])
def methodout():
    if request.method == 'POST':
        print('post')
        data = request.form
    else:
        print('get')
        data = request.args
    return render_template('method.html', data1 = data, data2 = request.method) 
    #http://127.0.0.1/method?name=hong&age=10

# get으로 들어올때도 받고 post로 들어올 때도 받겠다는 의미 기본값은 GET이다.->걍 /해서 호출하는거



@app.route('/fileupload', methods = ['GET', 'POST'])
def fileupload():
    if request.method =='GET':
        return render_template('fileinput.html')
    else:
        f = request.files['formFile']
        path = os.path.dirname(__file__)+'/upload/'+f.filename  # 실행하는 파일의 정보가 들어있다.__file__ app.py의 정보를 뽑아준다.
        print(path)
        f.save(path)  # 요 경로에 저장

        return redirect('/')



@app.route('/bloglist')
def bloglist():
    conn = db.dbconn()
    cursor = conn.cursor()
    sql = ''' select * from blog '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    print(rows)
    return render_template('bloglist.html', data = rows)

@app.route('/blogform', methods = ['GET', 'POST'])
def blogform():
    if request.method == 'GET':
        return render_template('blogform.html')
    else:
        f = request.files['formFile']
        path = os.path.dirname(__file__)+'/static/blog/img/'+f.filename
        print(path)
        f.save(path)
        print('저장성공')
        print(request.form)
        conn = db.dbconn()
        cursor = conn.cursor()
        sql = '''insert into blog (title, content, img_path) values(?,?,?)'''
        data = [request.form['title'], request.form['content'], '/static/blog/img/'+f.filename]
        cursor.execute(sql, data)
        conn.commit()
        conn.close()
        # 글을 db에 저장
        return redirect('/bloglist')

@app.route('/blog/<int:id>')
def blogcontent(id):
    conn = db.dbconn()
    cursor = conn.cursor()
    sql = ''' select * from blog where id=? '''
    cursor.execute(sql, id)
    rows = cursor.fetchone()
    conn.commit()
    conn.close()
    return render_template('blog_content.html', data = rows)

@app.route('/blogdelete/<int:id>')
def blogdelete(id):
    conn = db.dbconn()
    cursor = conn.cursor()
    sql = ''' delete blog where id=? '''
    cursor.execute(sql, id)
    conn.commit()
    conn.close()
    return redirect('/bloglist')

if __name__=='__main__':
    app.run(debug = True, port = 80)