import base64
import random
from threading import Thread
from flask import *
from flask_mysqldb import MySQL
from datetime import datetime
from flask_mail import Mail, Message
import os

app = Flask(__name__)
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = 'certificates'



app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'lendahand'
app.secret_key = "kenshin"  

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH']=10000000

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hrithikdas2nd@gmail.com'
app.config['MAIL_PASSWORD'] = 'xnkermlbeodmkwcz'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
mail.init_app(app)


mysql=MySQL(app)
 

@app.route("/")
def index():
    return render_template("home.html")


@app.route("/volunteerhomepage")
def volunteerhomepage():
    cur = mysql.connection.cursor()

        # Execute query
    cur.execute("select o.organisation_name,e.title,e.description from organisers o inner join event e on o.email=e.email where status=(%s)",['ongoing'])

        # Commit to DB
    ongoingevents = cur.fetchall()
    cur.execute("select * from event where status=(%s)",['upcoming'])
    upcomingevents = cur.fetchall()
    mysql.connection.commit()
    
    print(ongoingevents,upcomingevents)
        # Close 
    cur.close()
    return render_template("volunteerhomepage.html",ongoingevents=ongoingevents,upcomingevents=upcomingevents)

@app.route("/activeeventpage")
def activeEventPage():
    cur = mysql.connection.cursor()

        # Execute query
    cur.execute("select * from rough")

        # Commit to DB
    result = cur.fetchall()

    mysql.connection.commit()

        # Close connection
    cur.close()
    print(result)
    return render_template("activeEventpage.html",nums=result)

@app.route("/organisereventpage")
def organiserEventPage():
    cur = mysql.connection.cursor()

        # Execute query
    cur.execute("select * from rough")

        # Commit to DB
    result = cur.fetchall()

    mysql.connection.commit()

        # Close connection
    cur.close()
    print(result)
    return render_template("organisereventpage.html",nums=result)


@app.route("/rough")
def rough():
    cur = mysql.connection.cursor()

        # Execute query
    cur.execute("select * from rough")

        # Commit to DB
    result = cur.fetchall()

    mysql.connection.commit()

        # Close connection
    cur.close()
    return render_template("rough.html",nums=result)

@app.route("/volunteersignup", methods = ["GET","POST"])
def volunteersignup():
    print(request.data)
    # name = request.form['name']
    # email = request.form['email']
    # password = request.form['password']
    # phonenumber = request.form['phonenumber']
    # role = 'volunteer'
    # cur = mysql.connection.cursor()

    #     # Execute query
    # cur.execute("INSERT INTO users(name,email,password,phonenumber,role) VALUES(%s,%s,%s,%s,%s)",[name],[email],[password],[phonenumber],[role])

    # mysql.connection.commit()

    #     # Close connection
    # cur.close()

    return render_template("volunteersignup.html")


@app.route("/organisersignup")
def organisersignup():
    return render_template("organisersignup.html")


@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/signin")
def signin():
    if 'email' in session:  
        session.pop('email',None) 
    return render_template("signin.html")

@app.route("/organiserhomepage")
def organiserhomepage():
    cur = mysql.connection.cursor()

        # Execute query
    cur.execute("select * from event where status=(%s)",['completed'])
    events = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return render_template("organiserhomepage.html",events=events)

@app.route("/addevent")
def addevent():
    return render_template("add_event.html")

@app.route("/organiserprofile")
def organiserProfile():
    if 'email' in session:
        email = session['email']
        cur = mysql.connection.cursor()
        
        # Execute query
        cur.execute("select * from organisers where email=(%s)",[email])
        user = cur.fetchall()
        cur.execute("select count(*) from event where email=(%s) and status='completed'",[email])
        count = cur.fetchall()
        print(user)
        mysql.connection.commit()
        cur.close()
    
        return render_template("organiserprofile.html",user=user,count=count)
    return render_template("organiserprofile.html")

@app.route("/savevolunteer",methods = ["POST"])
def savevolunteer():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    phonenumber = request.form['phonenumber']
    location=request.form['location']
    cur = mysql.connection.cursor()

       
    cur.execute("INSERT INTO volunteers(name,email,password,phone_number,location) VALUES(%s,%s,%s,%s,%s)",[name,email,password,phonenumber,location])

    mysql.connection.commit()

        # Close connection
    cur.close()
    return render_template("signin.html")
@app.route("/saveorganiser",methods = ["POST"])
def saveorganiser():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    phonenumber = request.form['phonenumber']
    role = 'organiser'
    cur = mysql.connection.cursor()

        # Execute query
    cur.execute("INSERT INTO users(name,email,password,phone_number,role) VALUES(%s,%s,%s,%s,%s)",[name,email,password,phonenumber,role])
    
    mysql.connection.commit()

        # Close connection
    cur.close()
    return render_template("signin.html")

@app.route("/validate",methods = ["GET","POST"])
def validate():
    
    email = request.form['email']
    password = request.form['password']
   
  
    cur = mysql.connection.cursor()

        # Execute query
    cur.execute("select email,password from volunteers")
    volunteers = cur.fetchall()
    cur.execute("select email,password from organisers")
    organisers = cur.fetchall()
    mysql.connection.commit()

        # Close connection
    cur.close()
    for i in volunteers:
        if(i[0] == email and i[1] == password):
            if request.method == "POST":  
                session['email']=request.form['email']
                session['role']='volunteer'
            return volunteerhomepage()
    for i in organisers: 
        if(i[0] == email and i[1] == password):
            if request.method == "POST":  
                session['email']=request.form['email']
                session['role']='organiser'

            return organiserhomepage()
    
        
    return render_template("signin.html")

@app.route("/addorganisedevent",methods = ["POST"])
def addorganisedevent():
    title = request.form['title']
    description = request.form['description']
    #eventdate = request.form['date']
    eventdate = request.form['datepicker']
    status = request.form['status']
    location = request.form['location']
    #status = request.form.get('status')
    print(request.form.keys())
    #print(status)
    time = request.form['timer']
    time = time + ":00"
    scheduled_datetime = eventdate + " " + time
    date = datetime.now()
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    email = session['email']
    print(scheduled_datetime, date)
    cur = mysql.connection.cursor()

        # Execute query
    cur.execute("INSERT INTO event(email,title,description,scheduled_datetime,status) VALUES(%s,%s,%s,%s,%s)",[email,title,description,scheduled_datetime,status])
    location = request.form['location']
    cur.execute("SELECT email from volunteers WHERE location=(%s)", [location])
    mysql.connection.commit()
    
    data = cur.fetchall()
    l = []
    for i in data:
        l.append(i[0])
    for i in l:
        msg = Message('Event is going to happen in your Area', sender='hrithikdas2nd@gmail.com',
                          recipients=[i])
        msg.body = "Hey buddy, " + title + " event is going to happen at " + str(scheduled_datetime) 
        Thread(target=send_email, args=(app, msg)).start()

        # Close connection
    cur.close()
    return organiserUpcomingEventPage()

# @app.route("/upload",methods=["POST"])
# def upload():
#     file = request.files['image']
    
#     file.save(file.filename)
#     newfile = file.read()

#     cur = mysql.connection.cursor()
#     cur.execute("insert  completed_event_table(images) values(%s)",[newfile])
   
#     mysql.connection.commit()

#         # Close connection
#     cur.close()
#     return "Success "

# @app.route("/download")
# def download():
#     cur = mysql.connection.cursor()
#     cur.execute("select images from  completed_event_table")
#     images = cur.fetchall()
   
#     mysql.connection.commit()

#         # Close connection
#     cur.close()
#     return render_template("images.html",images=images)
@app.route('/success',methods = ["POST"])  
def success():  
    if request.method == "POST":  
        session['email']=request.form['email']  
    return render_template('success.html')  
 
@app.route("/organiserongoingevents",methods=["POST","GET"])
def ongoingevents():
    cur = mysql.connection.cursor()

        # Execute query
    cur.execute("select * from event where status='ongoing'")
    events = cur.fetchall()
    print(events)
    mysql.connection.commit()
    cur.close()
    return render_template("organiserongoingevents.html",events=events)

@app.route('/logout')  
def logout():  
    if 'email' in session:  
        session.pop('email',None)  
        return render_template('logout.html');  
    else:  
        return '<p>user already logged out</p>'  

@app.route("/upcomingeventpage")
def upcomingevent():
    return render_template("upcomingeventpage.html")

@app.route("/registered")
def registered():
    return "success"

@app.route("/email", methods=['GET', 'POST'])
def email():
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        conn = mysql.connection
        #city = request.form['city']
        cursor.execute("SELECT email from activity_registering_table WHERE status=%s", [1])
        conn.commit()
        data = cursor.fetchall()
        l = []
        for i in data:
            l.append(i[0])
        for i in l:
            msg = Message('Hello from the other side!', sender='hrithikdas2nd@gmail.com',
                          recipients=[i])
            msg.body = "Hey Hrithik, checking if the this msg is going to users registered for activity, lmk if it works"
            mail.send(msg)

        return "Message sent!"
    return render_template('mail.html')

@app.route("/volunteercompletedeventpagedetails/<string:title>")
def volunteercompletedeventpagedetails(title):
    cur = mysql.connection.cursor()

        # Execute query
    cur.execute("select * from event where title=(%s)",[title])
    events = cur.fetchone()
    cur.execute("select organiser from event_volunteer_table where event_title=(%s)",[title])
    organiser = cur.fetchone()
    print(organiser)
    cur.execute("select v.name,e.rating_by_organiser,e.volunteer_email,e.event_title from event_volunteer_table e inner join volunteers v on e.volunteer_email=v.email where e.event_title=(%s)",[title])
    nums = cur.fetchall()
    print(nums)
    print(session)
    mysql.connection.commit()
    cur.close()
    return render_template('volunteercompletedeventpagedetails.html',event=events,nums=nums,organiser=organiser)
@app.route("/volunteerupcomingeventpagedetails/<string:title>")
def volunteerupcomingeventpagedetails(title):
    cur = mysql.connection.cursor()
    cur.execute("select o.organisation_name,e.title,e.description,e.scheduled_datetime,e.location,o.phone_number from organisers o inner join event e on o.email=e.email where title=(%s)",[title])

        # Commit to DB
    organisername = cur.fetchone()
    

    mysql.connection.commit()
    cur.close()
    return render_template('volunteerupcomingeventpagedetails.html',event=organisername)
@app.route("/organiserupcomingeventpage")
def organiserUpcomingEventPage():
    cur = mysql.connection.cursor()

        # Execute query
    cur.execute("select * from event where status=(%s) and email=(%s)",['upcoming',session['email']])
    events = cur.fetchall()
    print(events)
    mysql.connection.commit()
    cur.close()
    return render_template('organiserupcomingeventpage.html',events=events)

@app.route("/volunteercompletedeventpage")
def volunteercompletedeventpage():
    cur = mysql.connection.cursor()

        # Execute query
    cur.execute("select title,description,scheduled_datetime,location,organiser from event inner join event_volunteer_table on title=event_title where volunteer_email=(%s) and status = 'completed'",[session['email']])
    events = cur.fetchall()
    print(events)
    mysql.connection.commit()
    cur.close()
    return render_template('volunteercompletedeventpage.html',event=events)

@app.route("/volunteerupcomingeventpage")
def volunteerupcomingeventpage():
    cur = mysql.connection.cursor()
    cur.execute("select o.organisation_name,e.title,e.description,e.scheduled_datetime,e.location,o.phone_number from organisers o inner join event e on o.email=e.email where status=(%s)",['upcoming'])

        # Commit to DB
    organisername = cur.fetchall()
    

    mysql.connection.commit()
    cur.close()
    return render_template('volunteerupcomingeventpage.html',event=organisername)

@app.route("/volunteerregisteredeventpage")
def volunteerregisteredeventpage():
    cur = mysql.connection.cursor()

        # Execute query
    cur.execute("select e.title,e.description,e.scheduled_datetime,e.location,v.organiser from event e inner join event_volunteer_table v on e.title=v.event_title where v.volunteer_email=(%s)",[session['email']])
    events = cur.fetchall()
    print(session)
    mysql.connection.commit()
    cur.close()
    return render_template('volunteerregisteredeventpage.html',events=events)

@app.route("/register/<string:title>")
def registerforevent(title):
    email = session['email']
    cur = mysql.connection.cursor()
    cur.execute("select organisation_name from organisers where email = (select email from event where title=(%s))",[title])
    organiser = cur.fetchone()
        # Execute query
    cur.execute("insert into event_volunteer_table(event_title,volunteer_email,organiser) values(%s,%s,%s)", [title,email,organiser[0]])
    events = cur.fetchall()
    print(events)
    mysql.connection.commit()
    cur.close()
    return volunteerregisteredeventpage()

@app.route("/volunteereventpage/<string:title>", methods=["POST","GET"])
def volunteereventpage(title):
    cur = mysql.connection.cursor()
    cur.execute("select o.organisation_name,e.title,e.description,e.scheduled_datetime,e.location,o.phone_number from organisers o inner join event e on o.email=e.email where title=(%s)",[title])

        # Commit to DB
    organisername = cur.fetchone()
    

    mysql.connection.commit()
    cur.close()
    return render_template("volunteereventpage.html",event=organisername)

@app.route("/organiserpreviouseventdetails/<string:title>")
def organiserpreviouseventpage(title):
    cur = mysql.connection.cursor()
    cur.execute("select * from event where title=(%s)",[title])
    event = cur.fetchone()
    cur.execute("select organisation_name,phone_number from organisers where email=(%s)",[event[0]])
    email = cur.fetchone()
    cur.execute("select v.name,vt.rating_by_organiser,vt.certificate_status,v.email from event_volunteer_table vt inner join event e on vt.event_title=e.title inner join organisers o on e.email=o.email inner join volunteers v on vt.volunteer_email=v.email where e.title=(%s)",[title])
    participants = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return render_template("organiserpreviouseventdetails.html",event=event,participants=participants,email=email)


@app.route("/organiserongoingeventdetails/<string:title>")
def organiserongoingeventdetails(title):
    cur = mysql.connection.cursor()
    cur.execute("select * from event where title=(%s)",[title])
    event = cur.fetchone()
    cur.execute("select organisation_name,phone_number from organisers where email=(%s)",[event[0]])
    email = cur.fetchone()
    cur.execute("select v.name,vt.rating_by_organiser,v.phone_number from event_volunteer_table vt inner join event e on vt.event_title=e.title inner join organisers o on e.email=o.email inner join volunteers v on vt.volunteer_email=v.email where e.title=(%s)",[title])
    participants = cur.fetchall()
    print(participants)
    mysql.connection.commit()
    cur.close()
    return render_template("organiserongoingeventdetails.html",event=event,participants=participants,email=email)

@app.route("/organiserupcomingeventdetails/<string:title>")
def organiserupcomingeventdetails(title):
    cur = mysql.connection.cursor()
    cur.execute("select * from event where title=(%s)",[title])
    event = cur.fetchone()
    cur.execute("select organisation_name,phone_number from organisers where email=(%s)",[event[0]])
    email = cur.fetchone()
    mysql.connection.commit()
    cur.close()
    return render_template("organiserupcomingeventdetails.html",event=event,email=email)


@app.route("/volunteerprofile")
def myprofile():
    if 'email' in session:
        email = session['email']
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("select * from volunteers where email=(%s)",[email])
        user = cur.fetchall()
        cur.execute("select count(*) from event where status='completed' and title in (select event_title from event_volunteer_table  where volunteer_email=(%s)) ",[email])
        
        count = cur.fetchall()
        cur.execute("select title,description,scheduled_datetime from event where status='completed' and title in (select event_title from event_volunteer_table  where volunteer_email=(%s)) ",[email])

        info=cur.fetchall()
        mysql.connection.commit()
        cur.close()
        print(user,count,info)
        return render_template("volunteerprofile.html",user=user,count=count,info=info)
@app.route("/resetpassword", methods=['GET', 'POST'])
def resetpassword():
    return render_template('resetpassword.html')
            
def send_email(app, msg):
    with app.app_context():
        mail.send(msg)


@app.route("/otp", methods=['GET', 'POST'])
def otp():
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        print('Hell')
        conn = mysql.connection
        email = request.form['email']
        session['email'] = email
        cursor.execute("SELECT email from volunteers WHERE email = (%s)", [email])
        conn.commit()
        data = cursor.fetchall()
        print(data)
        if email==data[0][0]:
            token= random.randint(111111,999999)
            session['token'] = token
            # cur = mysql.connection.cursor()
            # cur.execute('Insert into users (token) values (%s)', (token))
            # mysql.connection.commit()
            # cur.close()
            print('World')
            
            msg = Message('OTP', sender='hrithikdas2nd@gmail.com', recipients=[email])
            msg.body = "your otp to reset the password is "+str(token)
            mail.send(msg)
    return render_template('otp.html')

@app.route("/verifyotp", methods=['GET', 'POST'])
def verifyotp():
    otp = request.form['otp']
    email=session['email']
    token=session['token']
    print(type(otp),type(token),otp,token)
    if otp == str(token):
        print("hello")
        cursor = mysql.connection.cursor()
        conn = mysql.connection
        passw = request.form['passw']
        print(passw,email)
        cursor.execute("UPDATE volunteers set password=(%s) WHERE email=(%s)", [passw,email])
        conn.commit()
        cursor.close()
    return render_template('signin.html')


@app.route("/ratevolunteer/<string:email>/<string:title>", methods=["POST","GET"])
def ratevolunteer(email,title):
    rating=request.form['cars']
    cursor = mysql.connection.cursor()
    conn = mysql.connection
    cursor.execute("UPDATE event_volunteer_table set rating_by_organiser=(%s) WHERE volunteer_email=(%s) and event_title=(%s)", [rating,email,title])
    conn.commit()
    cursor.close()
    return organiserpreviouseventpage(title)

@app.route('/submitcertificate/<string:email>/<string:title>', methods = ['GET', 'POST'])
def submitcertificate(email,title):
   if request.method == 'POST':
        f = request.files['certificate']
        cursor = mysql.connection.cursor()
        conn = mysql.connection
        cursor.execute("UPDATE event_volunteer_table set certificate_status=(%s) WHERE volunteer_email=(%s) and event_title=(%s)", ["Issued",email,title])
        conn.commit()
        cursor.close()
        email = email[:-10]
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],  secure_filename(email + " + "+ title + f.filename[-4:])))
        return organiserpreviouseventpage(title)


@app.route('/downloadcertificate/<string:email>/<string:title>', methods = ['GET', 'POST'])
def downloadcertificate(email,title):
    if request.method == 'POST':  
        title = title.replace(" ","_")
        email = email[:-10]
        path = email + "__" + title + ".jpg"
        return send_file(os.path.join(app.config['UPLOAD_FOLDER'], path), as_attachment=True)
    

@app.route("/endtheevent/<string:title>")
def endtheevent(title):
    cursor = mysql.connection.cursor()
    conn = mysql.connection
    cursor.execute("UPDATE event set status='completed' WHERE title=(%s)", [title])
    conn.commit()
    cursor.close()
    return organiserhomepage()

@app.route("/editeventpage/<string:title>")
def editeventpage(title):
    cur = mysql.connection.cursor()
    cur.execute("select * from event where title=(%s)",[title])
    event = cur.fetchone()
    mysql.connection.commit()
    cur.close()
    print(event)
    return render_template("editeventpage.html",event=event)


@app.route("/editorganisedevent/<string:title>",  methods=["POST","GET"])
def editorganisedevent(title):
    title2 = request.form['title']
    description = request.form['description']
    #eventdate = request.form['date']
    eventdate = request.form['datepicker']
    status = request.form['status']
    location = request.form['location']
    #status = request.form.get('status')
    print(request.form.keys())
    #print(status)
    time = request.form['timer']
    time = time + ":00"
    scheduled_datetime = eventdate + " " + time
    date = datetime.now()
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    email = session['email']
    print(scheduled_datetime, date)
    cur = mysql.connection.cursor()

    cur.execute("delete from event where title=(%s)",[title])
       # Execute query
    cur.execute("INSERT INTO event(email,title,description,scheduled_datetime,status,location) VALUES(%s,%s,%s,%s,%s,%s)",[email,title2,description,scheduled_datetime,status,location])
    
    cur.close()
    return organiserUpcomingEventPage()


@app.route("/deletetheevent/<string:title>")
def deletetheevent(title):
    cur = mysql.connection.cursor()
    cur.execute("delete from event where title=(%s)",[title])
    mysql.connection.commit()
    cur.close()
    return organiserUpcomingEventPage()

app.run(debug=True)



