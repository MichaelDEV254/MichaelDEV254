import pymysql
connection=pymysql.connect(host="localhost",user="root",password="",database="finalproject")
from flask import*
app = Flask(__name__)
app.secret_key="dbsbdbfdfdbvjdbvbjbjvjjbv"
@app.route('/msg',methods=['POST','GET'])
def msg():
    if request.method=='POST':
        username=request.form['username']
        message_body=request.form['message_body']
        usersql = "select * from users where username=%s"
        usercursor=connection.cursor()
        usercursor.execute(usersql,(username))
        if message_body=="":
            return render_template("home.html",error="Message Cannot be empty")
        if usercursor.rowcount==0:
            return render_template("home.html",error="Login Required to send messages")
        else:
            sql = "insert into messages(message_body,username) values(%s,%s)"
            cursor=connection.cursor()
            cursor.execute(sql,(message_body,username))
            session['name']=username
            connection.commit()
            messagesql = 'select * from messages where message_cat= "sent" or 1=1'
            messagecursor = connection.cursor()
            messagecursor.execute(messagesql)
            if messagecursor.rowcount==0:
                return render_template("msg.html",message="No messages Available")
            else: #you can fetch one, fetch many...
                msg=messagecursor.fetchall() #create a variable to store messages in this case ,msg
                return render_template("announcements.html",mymessage=msg,message="Sent")
    else:
        messagesql = 'select * from messages where message_cat= "sent"'
        messagecursor = connection.cursor()
        messagecursor.execute(messagesql)
        msg = messagecursor.fetchall()
        return render_template("msg.html",mymessage=msg)
# create a new route
@app.route('/signup',methods=['POST','GET'])
def register():
    if request.method=='POST':
        username=request.form['username']
        user_email=request.form['user_email']
        user_phone=request.form['user_phone']
        user_password=request.form['user_password']
        confirm_recovery_ans=request.form['confirm_recovery_ans']
        confirm_password=request.form['confirm_password']
        recovery_quiz = request.form['recovery_quiz']
        recovery_ans = request.form['recovery_ans']
        user_pay = request.form['user_pay']
        user_bio = request.form['user_bio']
        user_location = request.form['user_location']
        user_website_link = request.form['user_website_link']
        user_skill_1 = request.form['user_skill_1']
        user_skill_2 = request.form['user_skill_2']
        user_skill_3 = request.form['user_skill_3']
        user_skill_4 = request.form['user_skill_4']
        user_skill_5 = request.form['user_skill_5']
        user_skill_6 = request.form['user_skill_6']
        user_skill_7 = request.form['user_skill_7']
        user_skill_8 = request.form['user_skill_8']
        user_skill_9 = request.form['user_skill_9']
        user_skill_10 = request.form['user_skill_10']
            # validation checks
        confirm_email_sql="select * from users where  user_email=%s"
        confirm_email_cursor=connection.cursor()
        confirm_email_cursor.execute(confirm_email_sql,(user_email))
        confirm_user_sql="select * from users where username=%s"
        confirm_user_cursor=connection.cursor()
        confirm_user_cursor.execute(confirm_user_sql,(username))
        if confirm_user_cursor.rowcount !=0 :
            return render_template("signup.html", error1=f"Username {username} is taken.Try a different username")
        elif confirm_email_cursor.rowcount !=0:
            return render_template("signup.html", error1="The email is already in use")
        elif " " in username:
            return render_template("signup.html",error1="username  must have one word")
        elif "@" not in user_email:
            return render_template("signup.html",error2="Email Must Have @")
        elif not user_phone.startswith("254"):
            return render_template("signup.html",error3="Phone Must start with 254***")
        elif len(user_password)<8:
            return render_template("signup.html",error4="Password must be atleast 8 characters")
        elif user_password != confirm_password:
            return render_template("signup.html",error5="Password Mismatch.Please Confirm Password")
        elif recovery_ans != confirm_recovery_ans:
            return render_template("signup.html",error6="Recovery answer does not match")

        else:
            sql="insert into users(username,user_email,user_phone,user_password,recovery_quiz,recovery_ans,user_pay,user_bio,user_location,user_website_link,user_skill_1,user_skill_2,user_skill_3,user_skill_4,user_skill_5,user_skill_6,user_skill_7,user_skill_8,user_skill_9,user_skill_10)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            #    create cursor -cursor is used to execute sql querry
            cursor=connection.cursor()

            #execute sql query
            cursor.execute(sql,(username,user_email,user_phone,user_password,recovery_quiz,recovery_ans,user_pay,user_bio,user_location,user_website_link,user_skill_1,user_skill_2,user_skill_3,user_skill_4,user_skill_5,user_skill_6,user_skill_7,user_skill_8,user_skill_9,user_skill_10))
            session["signed_up"] = username
            # commit
            connection.commit()
            return redirect("/signin")
    else:
            # add the sms code
            return render_template("signup.html",success="Account created sucessfully")
@app.route("/home",methods=['POST','GET'])
def home():
    # create some code to fetch products
    #  define the sql querry to be executed
    usersql = "select * from users where username ='mike' or 1+1"


    # cursor for user
    usercursor = connection.cursor()
    # execute the querry
    usercursor.execute(usersql)
    # execute smartphone sql
    # check if there's clithes in the database
    if usercursor.rowcount == 0:
        return render_template("home.html", message="No users Available")
    else:  # you can fetch one, fetch many...
        users = usercursor.fetchall()
        # create a variable to store users in this case ,user
        return render_template("home.html",myusers=users)

@app.route('/announcements')
def announcements():
    messagesql="select * from messages where message_cat='sent' or 1=1"
    messagecursor=connection.cursor()
    messagecursor.execute(messagesql)
    if messagecursor.rowcount==0:
        return render_template("announcements.html",message="No messages Available")
    else: #you can fetch one, fetch many...
        msg=messagecursor.fetchall() #create a variable to store messages in this case ,msg
        messagesql = "select * from messages where message_cat='sent' or 1=1"
        messagecursor = connection.cursor()
        messagecursor.execute(messagesql)
        msg = messagecursor.fetchall()
        return render_template("announcements.html",mymessage=msg)
@app.route('/all_users')
def all_users():
    all_userssql = "select * from users where user_skill_1 or user_skill_2 or user_skill_3 or user_skill_4 or user_skill_5 or user_skill_6 or user_skill_7 or user_skill_8 or user_skill_9 or user_skill_10 ='none' or 1=1 "
    all_userscursor=connection.cursor()
    all_userscursor.execute(all_userssql)
    if all_userscursor.rowcount==0:
        return render_template("/all_users",message="No record")
    else:
        my_all_users=all_userscursor.fetchall()
    return render_template("all_users.html",All_Users=my_all_users)
@app.route("/single_item/<username>")
def single_item(username):#pass the email as a parameter
    # create the sqlquerry
    #pass the value of user email as %s placeholder-it will take the actual email during querying
    sql_single_item='select * from users where username=%s'
    # create a cursor to execute the sql
    cursor_single=connection.cursor()
    # execute the query
    cursor_single.execute(sql_single_item,username)
    single_user=cursor_single.fetchone() #we only need one row

    # code for fetching similar items
    my_user_name=single_user[21]
    sqlother_users='select * from users where user_skill_1=%s or 1=1 LIMIT 9' #LIMIT 9
    cursorother_users=connection.cursor()
    cursorother_users.execute(sqlother_users,my_user_name)
    similar_users=cursorother_users.fetchall()
    return render_template("/single_item.html",one_user=single_user,more_users=similar_users)

@app.route("/jobs")
def jobs():
    jobsql="select * from jobs"
    jobcursor=connection.cursor()
    jobcursor.execute(jobsql)
    job=jobcursor.fetchall()
    return render_template("/jobs.html",myjob=job)

@app.route("/hookup/<employee_name>")
def hookup(employee_name):
    # create the sqlquerry
    #pass the value of user email as %s placeholder-it will take the actual email during querying
    sqlsingle_employee_name='select * from jobs where employee_name= %s'
    # create a cursor to execute the sql
    cursorsingle_employee_name=connection.cursor()
    # execute the query
    cursorsingle_employee_name.execute(sqlsingle_employee_name,employee_name)
    single_employee=cursorsingle_employee_name.fetchone() #we only need one row

    # code for fetching similar items
    my_employee=single_employee[1]
    sqlother_employees='select * from jobs where employee_name= %s  LIMIT 9' #LIMIT 9
    cursorother_employees=connection.cursor()
    cursorother_employees.execute(sqlother_employees,my_employee)
    similar_employees=cursorother_employees.fetchall()
    return render_template("/hookup.html",one_employee=single_employee,more_employees=similar_employees)

@app.route("/post",methods=['POST','GET'])
def post():
    if request.method=='POST':
        Job_name=request.form['Job_name']
        username = request.form['username']
        main_role=request.form['main_role']
        employee_name=request.form['employee_name']
        employee_contact=request.form['employee_contact']
        employee_email=request.form['employee_email']
        employee_website=request.form['employee_website']
        number_of_vacancies = request.form['number_of_vacancies']
        attatched_message = request.form['attatched_message']
        requirement_1 = request.form['requirement_1']
        requirement_2 = request.form['requirement_2']
        requirement_3 = request.form['requirement_3']
        requirement_4 = request.form['requirement_4']
        requirement_5 = request.form['requirement_5']
        requirement_6 = request.form['requirement_6']
        requirement_7 = request.form['requirement_7']
        requirement_8 = request.form['requirement_8']
        requirement_9 = request.form['requirement_9']
        requirement_10 = request.form['requirement_10']
        sql="select * from users where username=%s"
        cursor=connection.cursor()
        cursor.execute(sql,(username))
        connection.commit()
            # validation checks
        if " " in employee_email:
            return render_template("post.html",error="email  cannot have a whitespace")
        elif cursor.rowcount==0:
            return render_template("signin.html",error="You must login to post a job")
        elif " " in username:
            return  render_template("post.html",error="Intrussion Attempt was noticed.Admin was notified")
        elif "@" not in employee_email:
            return render_template("post.html",error="Email Must Have @")

        else:
            sql="insert into jobs(Job_name,main_role,employee_name,employee_contact,employee_email,employee_website,number_of_vacancies,attatched_message,requirement_1,requirement_2,requirement_3,requirement_4,requirement_5,requirement_6,requirement_7,requirement_8,requirement_9,requirement_10)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            #    create cursor -cursor is used to execute sql querry
            cursor=connection.cursor()

            #execute sql query
            cursor.execute(sql,(Job_name,main_role,employee_name,employee_contact,employee_email,employee_website,number_of_vacancies,attatched_message,requirement_1,requirement_2,requirement_3,requirement_4,requirement_5,requirement_6,requirement_7,requirement_8,requirement_9,requirement_10))
            # commit
            connection.commit()
            return render_template("/post.html", success="Job posted sucessfully")
            # add the sms code
    else:
        return render_template("/post.html")

@app.route("/signin",methods=['POST','GET'])
def signin():
    if request.method=='POST':
        username=request.form['username']
        user_password = request.form['user_password']
        sqlalchemy="select * from users where username=%s and user_password=%s"
        cursor=connection.cursor()
        cursor.execute(sqlalchemy,(username,user_password))
        if username=="MichaelDev" and user_password=="@SecretKey#MichaelDev254#":
            session['username'] = username
            session['admin']=username
            return render_template("admin.html",messages="You Logged in as Admin")
        elif cursor.rowcount==0:
            return render_template("signin.html",error="Wrong Password or username")
        else:
            session['username'] = username
            return redirect("/home")
    else:
        return render_template("signin.html",success="Welcome back")

@app.route("/")
def welcome():
    return render_template("welcome.html")
@app.errorhandler(404)
def not_found(e):
    return render_template('custom_page.html'), 404
@app.route("/report/<username>",methods=['POST','GET'])
def report(username):
    if request.method == 'POST':
        admin_inbox = request.form['admin_inbox']
        if admin_inbox=="":
            return render_template("report.html",error="Message Cannot be empty")
        else:
            sql = "insert into admin(admin_inbox,username) values(%s,%s)"
            cursor=connection.cursor()
            cursor.execute(sql,(admin_inbox,username))
            connection.commit()
            return render_template("report.html",message="Message Sent")
    return render_template("report.html")
@app.route("/admin")
def admin():
    return render_template("admin.html")
@app.route("/delete_users",methods=['POST','GET'])
def delete_users():
    all_userssql = "select * from users where user_skill_1 or user_skill_2 or user_skill_3 or user_skill_4 or user_skill_5 or user_skill_6 or user_skill_7 or user_skill_8 or user_skill_9 or user_skill_10 ='none' or 1=1 "
    all_userscursor = connection.cursor()
    all_userscursor.execute(all_userssql)
    if all_userscursor.rowcount == 0:
        return render_template("/all_users", message="No record")
    else:
        my_all_users = all_userscursor.fetchall()
    if request.method=='POST':
        a_password = request.form['a_password']
        username = request.form['username']
        passwordsql="select * from admin where a_password=%s"
        usersql="select * from users where username=%s"
        usercursor=connection.cursor()
        passwordcursor=connection.cursor()
        passwordcursor.execute(passwordsql,(a_password))
        usercursor.execute(usersql,(username))
        if passwordcursor.rowcount==0:
            return render_template("delete_users.html",error="Wrong Password. Admin Will be notified of the Login Attempt")
        elif usercursor.rowcount==0:
            return render_template("delete_users.html",error="Wrong Username. Admin Will be notified of the Delete Attempt")
        else:
            deletesql="DELETE FROM users WHERE username=%s"
            deletecursor = connection.cursor()
            deletecursor.execute(deletesql,(username))
            connection.commit()
            return render_template("delete_users.html", All_Users=my_all_users,message="Delete successful")
    else:
         return render_template("delete_users.html",All_Users=my_all_users)
@app.route("/delete_jobs",methods=['POST','GET'])
def messages():
    if request.method=='POST':
        a_password = request.form['a_password']
        main_role = request.form['main_role']
        employee_name = request.form['employee_name']
        job_name = request.form['job_name']
        passwordsql="select * from admin where a_password=%s"
        rolesql="select * from jobs where main_role=%s"
        employeesql = "select * from jobs where employee_name=%s"
        jobnamesql = "select * from jobs where job_name=%s"
        jobnamecursor=connection.cursor()
        jobnamecursor.execute(jobnamesql,(job_name))
        employeecursor = connection.cursor()
        employeecursor.execute(employeesql,(employee_name))
        rolecursor=connection.cursor()
        rolecursor.execute(rolesql, (main_role))
        passwordcursor=connection.cursor()
        passwordcursor.execute(passwordsql,(a_password))
        if passwordcursor.rowcount==0:
            return render_template("delete_jobs.html",error="Wrong Password. Admin Will be notified of the Intrusion Attempt")
        elif jobnamecursor.rowcount==0: #job position in the form
            return render_template("delete_jobs.html",error="Error!!!.Wrong Job Position")
        elif employeecursor.rowcount==0:
            return render_template("delete_jobs.html",error="Error!!!.Wrong Employee Name")
        elif rolecursor.rowcount==0:
            return render_template("delete_jobs.html",error="Error!!!.Wrong Job Role Name")
        else:
            deletesql="DELETE FROM jobs WHERE job_name=%s and employee_name=%s and main_role=%s"
            deletecursor = connection.cursor()
            deletecursor.execute(deletesql,(job_name,employee_name,main_role))
            connection.commit()
            jobsql = "select * from jobs"
            jobcursor = connection.cursor()
            jobcursor.execute(jobsql)
            job = jobcursor.fetchall()
            return render_template("delete_jobs.html",myjob=job,message="Delete successful")
    else:
        jobsql = "select * from jobs"
        jobcursor = connection.cursor()
        jobcursor.execute(jobsql)
        job = jobcursor.fetchall()
        return render_template("delete_jobs.html",myjob=job)
@app.route("/delete_messages",methods=['POST','GET'])
def delete_messages():
    if request.method=='POST':
        username=request.form['username']
        message_body=request.form['message_body']
        usersql = "select * from users where username=%s"
        usercursor=connection.cursor()
        usercursor.execute(usersql,(username))
        messagesql = 'select * from messages where message_body= %s'
        messagecursor = connection.cursor()
        messagecursor.execute(messagesql,(message_body))
        messagesql = 'select * from messages where message_cat= "sent" or 1=1'
        messagecursor = connection.cursor()
        messagecursor.execute(messagesql)
        msg = messagecursor.fetchall()
        # if pascursor.rowcount==0:
        #     return render_template("delete_messages.html",error="Wrong Password",mymessage=msg)
        if messagecursor.rowcount==0:
            return render_template("delete_messages.html",error="No Such messages Available",mymessage=msg)
        elif usercursor.rowcount==0:
            return render_template("delete_messages.html",error="You cannot delete other people's messages",mymessage=msg)
        else: #you can fetch one, fetch many...
            msg=messagecursor.fetchall() #create a variable to store messages in this case ,msg
            delsql = "DELETE FROM messages WHERE message_body=%s and username=%s"
            delcursor=connection.cursor()
            delcursor.execute(delsql,(message_body,username))
            return redirect("/delete_messages")
    else:
        messagesql = 'select * from messages where message_cat= "sent"'
        messagecursor = connection.cursor()
        messagecursor.execute(messagesql)
        msg = messagecursor.fetchall()
        return render_template("delete_messages.html",mymessage=msg)
@app.route("/account_deletion/<username>",methods=['POST','GET'])
def account_deletion(username):
    if request.method=='POST':
        user_password=request.form['user_password']
        passwordsql="select * from users where username=%s and user_password=%s"
        confirmsql="select * from users where username=%s"
        confirmcursor=connection.cursor()
        confirmcursor.execute(confirmsql,(username))
        passwordcursor=connection.cursor()
        passwordcursor.execute(passwordsql,(username,user_password))
        # code for single item
        sql_single_item = 'select * from users where username=%s'
        # create a cursor to execute the sql
        cursor_single = connection.cursor()
        # execute the query
        cursor_single.execute(sql_single_item, username)
        single_user = cursor_single.fetchone()  # we only need one row
        # code for fetching similar items
        my_user_name = single_user[21]
        one_user = single_user
        # end of single item
        active_user=request.form['active_user']
        if username != active_user:
            return render_template("account_deletion.html",error="You cannot delete an account which is not yours")
        elif confirmcursor.rowcount==0:
            return render_template("account_deletion.html",error="This username is not available. Refresh the page")
        elif passwordcursor.rowcount==0:
            return render_template("account_deletion.html",error="Wrong Password")
        else:
            deletesql = "DELETE FROM users WHERE user_password=%s and username=%s"
            deletecursor=connection.cursor()
            deletecursor.execute(deletesql,(user_password,username))
            session.clear()
            return render_template("home.html", error="Account deleted")
    return render_template("account_deletion.html")
@app.route("/admininbox")
def admininbox():
    sql="select * from admin"
    cursor=connection.cursor()
    cursor.execute(sql)
    inbox=cursor.fetchall()
    return render_template("admininbox.html",myinbox=inbox)
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/home')
if __name__ == '__main__':
    app.run(debug=True)