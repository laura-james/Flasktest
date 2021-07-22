from flask import Flask, render_template, request, flash
from random import choice
from werkzeug.utils import secure_filename
import sqlite3, random


web_site = Flask(__name__)
#https://pythonise.com/series/learning-flask/flask-configuration-files
#web_site.config['UPLOAD_FOLDER']="/uploads/"
#web_site.config['FLASK_DEBUG']=1
web_site.config.update(
    TESTING=True,
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/',
    UPLOAD_FOLDER =  "static/uploads/",
    DEBUG = True,
    ENV = 'development'
)
#print(web_site.config)
number_list = [
	100, 101, 200, 201, 202, 204, 206, 207, 300, 301, 302, 303, 304, 305, 307, 400, 401, 402, 403, 404, 405, 406, 408, 409, 410, 411, 412, 413, 414, 415,
	416, 417, 418, 421, 422, 423, 424, 425, 426,
	429, 431, 444, 450, 451, 500, 502, 503, 504, 506, 507, 508, 509, 510, 511, 599
]
score = 0 #added to when you get a song correct
#https://code-maven.com/python-flask-before-first-request
@web_site.before_first_request
def before_first_request():
    web_site.logger.info("before_first_request - this might be useful to set stuff up?")

@web_site.route('/')
def index():
	return render_template('index.html')

@web_site.route('/user/', defaults={'username': None})
@web_site.route('/user/<username>')
def generate_user(username):
	if not username:
		username = request.args.get('username')

	if not username:
		return 'Sorry error something, malformed request.'

	return render_template('personal_user.html', user=username)

@web_site.route('/page')
def random_page():
  return render_template('page.html', code=choice(number_list))

@web_site.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      url = web_site.config['UPLOAD_FOLDER'] + secure_filename(f.filename)
      f.save(url)
      #below works for text files
      #file = open(web_site.config['UPLOAD_FOLDER'] + secure_filename(f.filename),"r")
      #content = file.read()   
        
      return render_template('content.html', url=url) 
      #return 'file uploaded successfully'

@web_site.route("/allusers")
def allusers():
  con = sqlite3.connect('users.db')
  con.row_factory = sqlite3.Row
  cursor = con.cursor()

  sql = '''
      SELECT * FROM users 
      '''
  cursor.execute(sql)
  con.commit()

  rows = cursor.fetchall() 
 # for row in rows:
  #    print(row)
  return render_template('users.html', users=rows)

@web_site.route("/adduser")
def adduser():
  return render_template('adduser.html')

@web_site.route("/addusertodb",methods = ['GET', 'POST'])
def addusertodb():
  #https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
  if request.method == 'POST':
    #print(request.form["username"])
    #https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa
    sql3 = "INSERT INTO `users` (`username`, `password`, `email_address`, `first_name`, `last_name`) VALUES ('"+request.form["username"]+"', '"+request.form["password"]+"', 'test@gmail.com', 'Bob', 'Smith')"
    #TODO add parameter to prevent sql injection
    web_site.logger.info(sql3)
    con = sqlite3.connect('users.db')
    con.row_factory = sqlite3.Row  #allows us to use dictionary names rather than numbers
    #https://stackoverflow.com/questions/44009452/what-is-the-purpose-of-the-row-factory-method-of-an-sqlite3-connection-object
    cursor = con.cursor()
    cursor.execute(sql3)
    con.commit()
    return "adding user....."+request.form["username"]+"<a href='/allusers'>see all users</a>"
@web_site.route("/edit")
def edit():
  id = request.args.get('id')
  con = sqlite3.connect('users.db')
  con.row_factory = sqlite3.Row
  cursor = con.cursor()

  sql = ' SELECT * FROM users WHERE id = "'+id+'"'
  cursor.execute(sql)
  con.commit()

  rows = cursor.fetchall() 
 # for row in rows:
  #    print(row)
  return render_template('edit.html', user=rows)
  #return "You tried to edit user " + id

@web_site.route("/edituser",methods = ['GET', 'POST'])
def edituser():
  #https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
  if request.method == 'POST':
    #remember to refresh the page before resubmitting else there won't be any data
    print(request.form["username"])
    print(request.form["password"])
    for x,y in request.form.items():#iterates over the dictionary to show the key and the value
      print(x,y)
    
    #https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa
    sql3 = "UPDATE `users` SET `username`= '"+request.form["username"]+"',`password`='"+request.form["password"]+"', `email_address`='"+request.form["email"]+"', `first_name`='"+request.form["firstname"]+"', `last_name`='"+request.form["lastname"]+"' WHERE id = "+request.form["id"]
    #TODO add parameter to prevent sql injection
    web_site.logger.info(sql3)
    con = sqlite3.connect('users.db')
    con.row_factory = sqlite3.Row
    #https://stackoverflow.com/questions/44009452/what-is-the-purpose-of-the-row-factory-method-of-an-sqlite3-connection-object
    cursor = con.cursor()
    cursor.execute(sql3)
    con.commit()
    #return "editing user....."+request.form["username"]+"<a href='/allusers'>see all users</a>"
    #https://www.javatpoint.com/flask-flashing
    flash("Successfully updated "+request.form["username"],"information")  
    sql = '''
      SELECT * FROM users 
      '''
    cursor.execute(sql)
    con.commit()

    rows = cursor.fetchall()
    return render_template('users.html', users=rows)
@web_site.route("/delete")
def delete():
  id = request.args.get('id')
  con = sqlite3.connect('users.db')
  con.row_factory = sqlite3.Row
  cursor = con.cursor()

  sql = ' SELECT * FROM users WHERE id = "'+id+'"'
  cursor.execute(sql)
  con.commit()

  rows = cursor.fetchall() 
 # for row in rows:
  #    print(row)
  return render_template('delete.html', user=rows)
  #return "You tried to edit user " + id
@web_site.route("/deleteuser",methods = ['GET', 'POST'])
def deleteuser():
  #https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
  if request.method == 'POST':
    sql = "DELETE FROM `users`  WHERE id = "+request.form["id"]
    #TODO add parameter to prevent sql injection
    web_site.logger.info(sql)
    con = sqlite3.connect('users.db')
    con.row_factory = sqlite3.Row
    #https://stackoverflow.com/questions/44009452/what-is-the-purpose-of-the-row-factory-method-of-an-sqlite3-connection-object
    cursor = con.cursor()
    cursor.execute(sql)
    con.commit()
    #return "editing user....."+request.form["username"]+"<a href='/allusers'>see all users</a>"
    #https://www.javatpoint.com/flask-flashing
    flash("Successfully deleted "+request.form["username"],"information")  
    sql = '''
      SELECT * FROM users 
      '''
    cursor.execute(sql)
    con.commit()

    rows = cursor.fetchall()
    return render_template('users.html', users=rows)
@web_site.route("/play")
def playgame():
  things = getRandomSong()
  return render_template('game.html', artist=things[0],answer=things[1],letters=things[2])
@web_site.route("/musicgame",methods = ['GET', 'POST'])
def musicgame():
  global score
  if request.form["guess"]==request.form["answer"]:
    score = score + 1
    flash("Correct you have now scored "+str(score))  
    
  else:
    flash("Incorrect you have now scored "+str(score)) 
  things = getRandomSong()
  
  
  return render_template('game.html', artist=things[0],answer=things[1],letters=things[2])
def getRandomSong():
#generate a random number between 0 and length of file
  print("this will play the game...") 
  file = open("songlist.txt","r")
  songs = file.readlines()
  file.close()
  rand = random.randint(0,len(songs)-1)
  songandartist = songs[rand].strip()
  songbits = songandartist.split(",")
  #print(songbits[0])
  artist = songbits[0]
  answer = songbits[1]
  letters = ""
  songwords = songbits[1].split(" ")
  for i in range(len(songwords)):
    print(songwords[i][0]) #this gets the first letter of the first word
    letters = letters + " " +songwords[i][0]
  return [artist,answer,letters]

web_site.run(host='0.0.0.0', port=8080)