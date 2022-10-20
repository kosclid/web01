from flask import Flask, render_template, request, redirect
import os

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


if __name__=='__main__':
    app.run(debug = True, port = 80)