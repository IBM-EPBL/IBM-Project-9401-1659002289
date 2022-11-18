from flask import Flask,render_template, request, jsonify, session, redirect
#from flask_mysqldb import MySQL
from utils import category, find
from flask import cli
import ibm_db
import ibm_boto3
from ibm_botocore.client import Config, ClientError

COS_ENDPOINT="https://s3.jp-tok.cloud-object-storage.appdomain.cloud"
COS_API_KEY_ID="t81QlQrO4G_j-QNhbFWbI3QKQqsBgDCAH559eJ3v9MQK"
COS_INSTANCE_CRN="crn:v1:bluemix:public:cloud-object-storage:global:a/22e0dc49422e4859bd2e7165396ce75a:cafe19de-eb19-4229-86d9-0204fcb0f8ff::"



# Create resource https://s3.ap.cloud-object-storage.appdomain.cloud
cos = ibm_boto3.resource("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)

"""def get_bucket_contents(bucket_name):
    print("Retrieving bucket contents from: {0}".format(bucket_name))
    try:
        files = cos.Bucket(bucket_name).objects.all()
        files_names = []
        for file in files:
            files_names.append(file.key)
            print("Item: {0} ({1} bytes).".format(file.key, file.size))
        return files_names
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve bucket contents: {0}".format(e))"""

#cli.show_server_banner = lambda *_: None

app = Flask(__name__)
app.secret_key = "vani" 

#cloud
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=824dfd4d-99de-440d-9991-629c01b3832d.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30119;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=tvb74810;PWD=EdGcG242OX2nZ522;",'','')

#mysql
"""app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'
 
mysql = MySQL(app)"""

@app.route('/')
def index():
   #files = get_bucket_contents('flaskapp123')
   return render_template('index.html') #, files = files

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
         #cursor = mysql.connection.cursor()
         #cursor.execute('INSERT INTO user(email, password) VALUES(%s, %s)',(email, password))
         #mysql.connection.commit()

         sql = "SELECT * FROM USER WHERE EMAIL=?"
         stmt = ibm_db.prepare(conn, sql)
         ibm_db.bind_param(stmt,1,email)
         ibm_db.execute(stmt)
         user = ibm_db.fetch_assoc(stmt)

         if user:
            msg = "User already exist!!"
         else:
            jj
            sql = "INSERT INTO user(email, password) VALUES(?, ?)"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, email)
            ibm_db.bind_param(stmt, 2, password)
            ibm_db.execute(stmt)
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
         #cursor = mysql.connection.cursor()
         #sql = "SELECT * FROM USER WHERE EMAIL=%s AND PASSWORD=%s",(email, password)
         #cursor.execute(sql)
         #data = cursor.fetchone()
         #dbemail = data[1]
         #dbpassword = data[2]
         sql = "SELECT * FROM USER WHERE EMAIL=?"
         stmt = ibm_db.prepare(conn, sql)
         ibm_db.bind_param(stmt,1,email)
         ibm_db.execute(stmt)
         user = ibm_db.fetch_tuple(stmt)

         #if password == dbpassword:  
         if user[2]==password:
            session['status']="ok"
            return render_template("home.html")
            #return redirect("http://127.0.0.1/home")
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

#search
@app.route('/search', methods = ['POST', 'GET'])
def search():
   if request.method == 'POST':
      if 'status' in session:
         sr = request.form['search']
         news_articles = find(sr)
         return render_template("news.html", news_articles=news_articles)
      else:
         msg = "Please Login!!"
         return render_template("result.html", msg = msg)

if __name__ == '__main__':
   app.run(port='90', debug=True)

#docker build -t docker_flask .

