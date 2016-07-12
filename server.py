import os,sys
from flask import Flask,render_template,request
import psycopg2
import base64


# Read port selected by the cloud for our application
conn = psycopg2.connect(dbname='XXXXX', user='XXXXX', host='XXXXXX',port='XXXXXX', password='XXXXXX')

app = Flask(__name__)
port = int(os.getenv('PORT', 8000))
cur = conn.cursor()
tmp="tmp.txt"
tmp1="tmp1.txt"
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/authenticate',methods=['GET','POST'])
def authentcate():
    global username
    username= request.form['userid']
    password = request.form['pass']
    try:
        cur.execute("select username,password from user_details where username = %s", [username])
        rows = cur.fetchall()
        for row in rows:
            dbuser = row[0]
            dbpass = row[1]
        if dbpass == password:
            return render_template('index1.html',username=username)
        else:
            return "Login Failed"
    except:
        conn.commit()
        return "User Details are Invalid"

@app.route('/upload',methods=['GET','POST'])
def upload():
    return render_template('upload.html',username=username)
@app.route('/download')
def download():
    return render_template('download.html')

@app.route('/final',methods=['GET','POST'])
def fina():
    file=request.files['fileupload']
    dstat=request.form['desc']
    filename = file.filename
    tmp11 = open(tmp1, 'w')
    tmp11.write(file.read())
    tmp11.close()
    filesize= os.path.getsize(tmp1)
    #################fetch Maxsize################################
    cur.execute("select maxsize from user_details where username = %s", [username])
    rows = cur.fetchall()
    for row in rows:
        file_size_value = row[0]
    print file_size_value


    file_content = open(tmp1, "rb").read()
    en_contents = base64.b64encode(file_content)
    if filesize< file_size_value:
        if dstat != '1':
            cur.execute("INSERT INTO file_details values(%s,%s,%s,%s,%s,%s)",(id, filename, filesize,en_contents,dstat,username))
            conn.commit()
        else:
            cur.execute("INSERT INTO file_details(id,file_name,file_size,file_content,username) VALUES (%s,%s,%s,%s,%s)",(id,filename,filesize,contents,username))
            conn.commit()
    else:
        return "USER FILE SIZE EXCEEDED"
    return "FILE UPLOADEDED SUCCESSFULLY"
@app.route('/downloadfile',methods=['GET','POST'])
def downloadfile():
    filename=request.form['fname']
    username=request.form['uname']
    downloadedfile="download" + filename
    #### Checking if user exists ######
    try:
        cur.execute("select username from user_details where username = %s", [username])
        rows = cur.fetchone()
        dbusr = rows[0]
        if not dbusr:
            cur.execute("select file_name from file_details where file_name =%s and username=%s", [filename,username])
            filerow=cur.fetchone()
            dbfilename=filerow[0]
            if not dbfilename:
                cur.execute("select file_content from file_details where file_name=%s amd username=%s",[filename,username])
                contentrows=cur.fetchone()
                en_contents=contentrows[0]
                decrypted_data = en_contents.decode('base64')
                file = open(downloadedfile, 'w')
                file.write(str(decrypted_data))
                file.close()
            else:
                return "File name does not exist"
        else:
            return "Username does not exist"
    except:
        conn.commit()
        return "User Details are Invalid"


if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=int(port)) For running it in local
    app.run(debug=True)  ## for running it in IBM Bluemix Cloud
