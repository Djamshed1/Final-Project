import requests as requests
from pythonFiles import  app
from flask import render_template,request,json,session,redirect
from sqlalchemy import *
from pythonFiles import Sqlalchemy,myConnection
@app.route('/searchBookByIsdn',methods=['post','get'])
def searchBookByIsdn():
    isdn = request.form['isdn']
    selectAllUsersBook = select([Sqlalchemy.BookCatalogue]).where(
        Sqlalchemy.BookCatalogue.c.user_id == session['userID'])
    reAllBooks = myConnection.connection.execute(selectAllUsersBook)
    result = []
    for item in reAllBooks:
        result.append(dict(item))

    if isdn =='':
        return render_template('index.html',books=result, info="Please insert ISDN", errorCode=-1)

    url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:'
    r = requests.get(url+str(isdn))
    if r.status_code != 200:
        return  render_template('index.html',books=result,info="Problem with Google API",errorCode=-1)
    json1 = json.loads(r.content)
    if json1['totalItems'] == 0:
        return render_template('index.html',books=result, info="No book was found", errorCode=-1)
    author = ''
    for item in json1['items'][0]['volumeInfo']['authors']:
        author= author  + item + " "
    title = json1['items'][0]['volumeInfo']['title']

    page_count = json1['items'][0]['volumeInfo']['pageCount']
    if "averageRating" in json1['items'][0]['volumeInfo'].keys():
        average_rating = json1['items'][0]['volumeInfo']['averageRating']
    else:
        average_rating="No average rating"
    ins = insert(Sqlalchemy.BookCatalogue).values(
        title= title,
        author = author,
        page_count = page_count,
        average_rating = str(average_rating),
        user_id= session['userID']
    )
    myConnection.connection.execute(ins)

    selectAllUsersBook = select([Sqlalchemy.BookCatalogue]).where(
        Sqlalchemy.BookCatalogue.c.user_id == session['userID'])
    reAllBooks = myConnection.connection.execute(selectAllUsersBook)
    result = []
    for item in reAllBooks:
        result.append(dict(item))

    return render_template('index.html',books=result, errorCode=1)

@app.route('/bookDelete/<int:id>')
def bokkDelete(id):

    de = delete(Sqlalchemy.BookCatalogue).where(Sqlalchemy.BookCatalogue.c.id == id)
    myConnection.connection.execute(de)
    return redirect('index')