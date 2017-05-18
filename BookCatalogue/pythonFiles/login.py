

from pythonFiles import  app
from flask import  render_template,request,session,redirect
from sqlalchemy import  *
from pythonFiles import Sqlalchemy
from pythonFiles import myConnection
@app.route('/login')
def login():

    return render_template('login.html')

@app.route('/login/log',methods=['post','get'])
def loginLog():

    username = request.form['username']
    password = request.form['password']
    se = select([Sqlalchemy.Users]).where(and_(Sqlalchemy.Users.c.username == username,Sqlalchemy.Users.c.password == password))
    re = myConnection.connection.execute(se).first()
    if re == None:
        return render_template('login.html',info = 'Username or password are incorrect', k=1)
    session['userID'] = re['id']
    return  redirect('/index')

@app.route('/index', methods=['POST','GET'])
def index():
    selectAllUsersBook = select([Sqlalchemy.BookCatalogue]).where(
        Sqlalchemy.BookCatalogue.c.user_id == session['userID'])
    reAllBooks = myConnection.connection.execute(selectAllUsersBook)
    result = []
    for item in reAllBooks:
        result.append({'title': item['title'], "author": item['author'], "page_count": item['page_count'],
                       'average_rating': item['average_rating'], "id": item['id']})
    return render_template('index.html', books=result)

@app.route('/logout')
def logout():
    session.clear()

    return redirect("login")