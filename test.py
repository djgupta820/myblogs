from hashlib import md5
from mysql import connector
from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = "auth_token"

app.route("/")
def index():
    return render_template('test.html')

def fun():
    try:
        mydb = connector.connect(host="localhost", port=3310, user="root", password="djgupta", database="work")
        print("connected")
        curr = mydb.cursor()
        usern = "john123"
        passwd = 'john123'
        passwd = md5(passwd.encode('utf-8'))
        passwd = passwd.hexdigest()
        curr.execute("select * from users where username='" + usern + "' and password='" + passwd + "';")
        
        res = curr.fetchall()
        print(res)
        if res:
            print("logged in")
        else:
            print("not logged in")
        # for r in res:
        #     print(r)
    except Exception as e:
        print(str(e))

def fun1():
    try:
        conn = connector.connect(host="localhost", port=3310, user="root", password="djgupta", database="work")
    except Exception as e:
        print("Error: ", str(e))

    if conn:
        cur = conn.cursor()
        cur.execute("select * from blogs;")
        results = cur.fetchall()
        for result in results:
            print(result[0], result[1], result[2], result[3], result[4])
    else:
        pass

if __name__ == "__main__":
    app.run()