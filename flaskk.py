from re import U
from flask import Flask, flash, redirect, render_template, request, url_for, make_response, session
from mysql import connector
from hashlib import md5


app = Flask(__name__)
app.secret_key = 'authentication'       # for creating session


@app.route('/')
def land():
    return render_template('land.html')


@app.route('/index')
def index():
    try:
        conn = connector.connect(host="localhost", port=3310, user="root", password="djgupta", database="work")
    except Exception as e:
        print("Error: ", str(e))

    if conn:
        cur = conn.cursor()
        cur.execute("select * from blogs order by date_time desc;")
        results = cur.fetchall()
        conn.close()
        if results:
            context = {
                'results':results
            }
    else:
        context = {
            'results':'No data'
        }

    return render_template('index.html', **context)
    

@app.route("/login")
def login():
    return render_template('login.html')

@app.route('/_login', methods=['GET', 'POST'])
def _login():
    error = None

    if request.method == "POST":
        user_authenticated = False

        usern = request.form['username']
        passwd = request.form['password']

        # Hashing password
        passwd = md5(passwd.encode("utf-8"))
        passwd = passwd.hexdigest()
        
        try:
            conn = connector.connect(host="localhost", port=3310, user="root", password="djgupta", database="work")
        except Exception as e:
            print(str(e))
            return redirect(url_for('login_error'))
            
        if conn:
            cur = conn.cursor()
            cur.execute("select * from users where username='" + usern + "' and password='" + passwd + "';")
            user_exist = cur.fetchall()
            conn.close()
            if user_exist:
                flash("Logged In Successfull!")
                session['user_name'] = usern
                resp = make_response(redirect(url_for('index')))
                resp.set_cookie('username', usern)
                # session['username'] = usern
                print(session['user_name'])
                return resp
            else:
                return redirect(url_for('login_error'))
        else:
            print("Cannot connect to database")
            return redirect(url_for('login_error'))
    else:
        return redirect(url_for('login'))



@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        usern = request.form['username']
        email = request.form['email']
        passwd = request.form['password']
        cpasswd = request.form['cpassword']
        chk = request.form.get('check')
        
        if passwd != cpasswd:
            return redirect(url_for('register_error'))
        elif not chk:
            return redirect(url_for('register_error'))
        else:
            try:
                conn = connector.connect(host="localhost", port=3310, user="root", password="djgupta", database="work")
            except Exception as e:
                print("Error:", str(e))
                return redirect(url_for('register'))

        if conn:
            cur = conn.cursor()
            passwd = passwd.encode('utf-8')
            passwd = md5(passwd)
            passwd = passwd.hexdigest()
            q = """
                insert into users(
                    first_name, 
                    last_name, 
                    username, 
                    email, 
                    password
                    ) 
                values(
                    '{}','{}','{}','{}','{}'
                );
                """.format(fname,lname,usern,email,passwd)
            cur.execute(q)
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        else:
            print("oops... database connection error")
            return redirect(url_for('register'))
    else:
        return redirect(url_for('register'))

@app.route('/add_post')
def add_post():
    if session.get('user_name') is not None:
        return render_template('add_post.html')
    else:
        return redirect(url_for('login_required'))


@app.route('/addPost', methods=['GET', 'POST'])
def addPost():
    if session.get('user_name') is not None:
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']

            try:
                conn = connector.connect(host="localhost", port=3310, user="root", password="djgupta", database="work")
            except Exception as e:
                print("error:", str(e))
            
            if conn:
                cur = conn.cursor()
                cur.execute("insert into blogs(poster, title, content) values('" + request.cookies.get('username') + "','" + title + "','" + content + "');")
                conn.commit()
                cur.execute("update users set total_posts = total_posts + 1 where username='" + session.get('user_name') + "';")
                conn.commit()
                conn.close()
                return redirect(url_for('index'))
            else:
                return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login_required'))

@app.route('/profile')
def profile():
    if session.get('user_name') is not None:
        try:
            conn = connector.connect(host="localhost", port=3310, user="root", password="djgupta", database="work")
        except Exception as e:
            print("error:", str(e))

        if conn:
            cur = conn.cursor()
            cur.execute('select * from users where username="' + str(request.cookies.get('username')) + '";')
            result = cur.fetchone()
            conn.close()
            context = {
                'result':result
            }
            return render_template('profile.html', **context)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login_required'))


@app.route('/logout')
def logout():
    session.pop('user_name')
    return render_template('logout.html')


@app.route('/viewblog', methods=['GET', 'POST'])
def viewblog():
    # if session.get('user_name') is not None:
    if request.method == 'POST':
        post_id = request.form['post_id']
            # print(Fore.RED + str(post_id))
        try:
            conn = connector.connect(host="localhost", port=3310, user="root", password="djgupta", database="work")
        except Exception as e:
            print("Errot:",str(e))
        if conn:
            cur = conn.cursor()
            cur.execute("select * from blogs where id = " + str(post_id) + ";")
            result = cur.fetchone()
            conn.close()
            context = {
                    'result':result
                }
            return render_template('viewblog.html', **context)
        else:
            return render_template('viewblog.html')
    else:
        return render_template('viewblog.html')
    

@app.route('/myblogs')
def myblogs():
    if session.get('user_name') is not None:
        usern = session.get('user_name')
        try:
            conn = connector.connect(host="localhost", port=3310, user="root", password="djgupta", database="work")
        except Exception as e:
            print("Error:", str(e))
        
        if conn:
            cur = conn.cursor()
            q = "select b.id, b.poster, b.title, b.content, b.date_time from blogs b inner join users u on b.poster = u.username where u.username = '" + usern + "';"
            cur.execute(q)
            results = cur.fetchall()

            q1 = "select total_posts from users where username = '" + usern + "';"
            cur.execute(q1)
            total_post = cur.fetchone()
            conn.close()
            if results:
                context = {
                    'results':results,
                    'tp':total_post
                }
                return render_template('myblogs.html', **context)
            else:
                return render_template('myblogs.html')
        else:
            context = {
                'results':"oops... database connection error"
            }
            return render_template('myblogs.html', **context)
    else:
        return redirect(url_for('login_required'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keyword = request.form['query']
        try:
            conn = connector.connect(host="localhost", port=3310, user="root", password="djgupta", database="work")
        except Exception as e:
            print("Error:", str(e))
            
        if conn:
            cur = conn.cursor()
            cur.execute("select * from blogs where title like '%" + keyword + "%';")
            results = cur.fetchall()
            conn.close()
            if results:
                context = {
                        'results':results
                    }
                return render_template('results.html', **context)
            else:
                context = {
                        'results':None
                    }
                return render_template('results.html', **context)
        else:
            context = {
                    'results':"oops... Database connection error"
                }
            return render_template('results.html', **context)
    else:
        return redirect(url_for('index'))


@app.route('/edit_post', methods=['GET', 'POST'])
def edit_post():
    error = None
    if session.get('user_name') is not None:
        if request.method == 'POST':
            postid = request.form['post_id']
            try:
                conn = connector.connect(host="localhost", port=3310, user="root", password="djgupta", database="work")
            except Exception as e:
                print("oops... Database connection error!")
            
            if conn:
                cur = conn.cursor()
                cur.execute("select * from blogs where id = '" + postid + "';")
                result = cur.fetchone()
                conn.close()
                context = {
                    'result':result
                }
                return render_template('edit_post.html', **context)
            else:
                error="oops... cannot connect to database!"
                return render_template('myblogs.html', error=error)
        else:
            return render_template('myblogs.html')
    else:
        return redirect(url_for('login_required'))


@app.route('/editPost', methods=['GET', 'POST'])
def editPost():
    if request.method == 'POST':
        post_id = request.form['post_id']
        title = request.form['title']
        content = request.form['content']
        try:
            conn = connector.connect(host='localhost', port=3310, user="root", password="djgupta", database="work")
        except Exception as e:
            print("Error:", str(e))

        if conn:
            cur = conn.cursor()
            cur.execute("update blogs set title='" + title + "', content='" + content + "' where id = " + post_id + ";")
            conn.commit()
            conn.close()
            return redirect(url_for('myblogs'))
        else:
            error="oops... cannot connect to database!"
            return render_template('myblogs.html', error=error)

    else:
        return redirect(url_for('myblogs'))


@app.route('/delete_post', methods=['GET', 'POST'])
def delete_post():
    if session.get('user_name') is not None:
        if request.method == 'POST':
            post_id = request.form['post_id']
            try:
                conn = connector.connect(host="localhost", port=3310, user="root", password="djgupta", database="work")
            except Exception as e:
                print("Error: ", str(e))

            if conn:
                cur = conn.cursor()
                cur.execute("delete from blogs where id = " + post_id)
                conn.commit()
                cur.execute("update users set total_posts + total_posts - 1;")
                conn.commit()
                conn.close()
                return render_template('err_succ/post_delete.html')
            else:
                print('oops... Database connection error')
                return redirect(url_for('myblogs'))
        else:
            return redirect(url_for('myblogs'))
    else:
        return redirect(url_for('login_required'))


@app.route('/delete_success')
def delete_success():
    return render_template('err_succ/del_confirm')


@app.route('/change_password')
def change_password():
    if session.get('user_name') is not None:
        return render_template('change_password.html')
    else:
        return redirect(url_for('login_required'))


@app.route('/change_passwd', methods=['GET', 'POST'])
def change_passwd():
    if session.get('user_name') is not None:
        if request.method == 'POST':
            passwd = request.form['password']
            cpasswd = request.form['cpassword']
            
            if passwd != cpasswd:
                return redirect(url_for('change_password_error'))
            else:
                passwd = md5(passwd.encode('utf-8'))
                passwd = passwd.hexdigest()
                try:
                    conn = connector.connect(host="localhost", port=3310, user="root", password="djgupta", database="work")
                except Exception as e:
                    print("Error: ", str(e))

                if conn:
                    cur = conn.cursor()
                    cur.execute("update users set password = '" + passwd + "' where username = '" + session.get('user_name') + "';")
                    conn.commit()
                    conn.close()
                    return redirect(url_for('password_change_success'))
                else:
                    print('oops... Database connection error')
                    return redirect(url_for('change_password'))
        else:
            return redirect(url_for('change_password'))
    else:
        return redirect(url_for('login_required'))

            

###########################################################################################
# Functions for all the error and success messages                                        #
###########################################################################################

# All error messages
# login error
@app.route('/login_error')
def login_error():
    return render_template('err_succ/login_error.html')

# Login required error
@app.route('/login_required')
def login_required():
    return render_template('err_succ/login_require.html')
# Regietration Error
@app.route('/register_error')
def register_error():
    return render_template('err_succ/reg_err.html')


# All Success messages
# Register Success
@app.route('/register_success')
def register_success():
    return render_template('err_succ/reg_suc.html')


# this is a testing function
@app.route('/test')
def test():
    return render_template('test.html')


# All Password errors and successes
#password not match
@app.route('/change_password_error')
def change_password_error():
    return render_template('err_succ/password_error.html')


@app.route('/password_change_success')
def password_change_success():
    return render_template('err_succ/password_success.html')



if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')