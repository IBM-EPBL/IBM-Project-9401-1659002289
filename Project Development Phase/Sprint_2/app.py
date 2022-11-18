from flask import Flask,render_template, request, jsonify, session, redirect
from flask_mysqldb import MySQL
from utils import category, find
from flask import cli

#cli.show_server_banner = lambda *_: None

app = Flask(__name__)
app.secret_key = "vani" 

#mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'
 
mysql = MySQL(app)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/register')
def register():
   return render_template('register.html')

@app.route('/reg_res', methods = ['POST', 'GET'])
def reg_res():
    if request.method == 'GET':
         msg = "Please Login!!"
         return render_template("result.html", msg = msg)     
    
    if request.method == 'POST':
      try:
         email = request.form['email']
         password = request.form['password']
         cursor = mysql.connection.cursor()
         cursor.execute('INSERT INTO user(email, password) VALUES(%s, %s)',(email, password))
         mysql.connection.commit()
         msg = "User added successfully"

      except:
         msg = "error!! Can't add user"
         cursor.rollback()
      finally:
         return render_template("result.html", msg = msg)
         cursor.close()

@app.route("/login")
def login():
   return render_template('login.html')

@app.route("/log_res", methods = ['POST', 'GET'])
def log_res():
   if request.method == 'GET':
      msg = "Invalid Credentials!!"
      return render_template("result.html", msg = msg)
   
   if request.method == 'POST':
      try:
         email = request.form['email']
         password = request.form['password']
         cursor = mysql.connection.cursor()
         sql = "SELECT * FROM USER WHERE EMAIL=%s AND PASSWORD=%s",(email, password)
         cursor.execute(sql)
         data = cursor.fetchone()
         dbemail = data[1]
         dbpassword = data[2]

         if password == dbpassword:  
            session['status']="ok"
            return render_template("home.html")
         else:
            msg = "Invalid Credentials!!"
            return render_template("result.html", msg = msg)
            
      except TypeError as e:
         msg = "Invalid Credentials!!"
         return render_template("result.html", msg = msg)

@app.route('/logout')  
def logout():  
    if 'status' in session:  
        session.pop('status',None)  
        msg = "logout successful!!"
        return render_template("result.html", msg = msg) 
    else:  
        msg = "User already logged out!!"
        return render_template("result.html", msg = msg)

@app.route('/home')  
def getVariable():  
   if 'status' in session:  
      return render_template('home.html')
   else:
      msg = "Please Login!!"
      return render_template("result.html", msg = msg)
 
#countries
"""@app.route('/india')
def india():   
   news_articles = country("in")
   return render_template("news.html", news_articles=news_articles)"""

#category
@app.route('/entertainment')
def entertainment():
   if 'status' in session:
      news_articles = category("in","entertainment")
      return render_template("news.html", news_articles=news_articles, cat="Entertainment")
   else:
      msg = "Please Login!!"
      return render_template("result.html", msg = msg)

@app.route('/sports')
def sports():
   if 'status' in session:
      news_articles = category("in","sports")
      return render_template("news.html", news_articles=news_articles, cat="Sports")
   else:
      msg = "Please Login!!"
      return render_template("result.html", msg = msg)

@app.route('/technology')
def technology():
   if 'status' in session:
      news_articles = category("in","technology")
      return render_template("news.html", news_articles=news_articles, cat="Technology")
   else:
      msg = "Please Login!!"
      return render_template("result.html", msg = msg)

@app.route('/science')
def science():
   if 'status' in session:
      news_articles = category("in","science")
      return render_template("news.html", news_articles=news_articles, cat="Science")
   else:
      msg = "Please Login!!"
      return render_template("result.html", msg = msg)

@app.route('/health')
def health():
   if 'status' in session:
      news_articles = category("in","health")
      return render_template("news.html", news_articles=news_articles, cat="Health")
   else:
      msg = "Please Login!!"
      return render_template("result.html", msg = msg)

@app.route('/business')
def business():
   if 'status' in session:
      news_articles = category("in","business")
      return render_template("news.html", news_articles=news_articles, cat="Business")
   else:
      msg = "Please Login!!"
      return render_template("result.html", msg = msg)


if __name__ == '__main__':
   app.run(port='90', debug=True)

#docker build -t docker_flask .

