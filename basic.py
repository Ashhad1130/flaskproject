from flask import Flask,render_template,request,redirect, url_for, session
from flaskext.mysql import MySQL
from flask_login import login_required
from pymysql.cursors import DictCursor


import re
app=Flask(__name__)

#Connection to mysql
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Ashhad@1'
app.config['MYSQL_DATABASE_DB'] = 'OlympicDB'
app.secret_key = 'mysecretkey'

mysql = MySQL(cursorclass=DictCursor)

mysql.init_app(app)


#Route
@app.route("/")
def index():
    conn = mysql.connect()
    cursor =conn.cursor()
    query = "CREATE TABLE IF NOT EXISTS Athlete( Athlete_ID int(11) NOT NULL,Athlete_FirstName varchar(45) NOT NULL,Athlete_LastName varchar(45) NOT NULL,Athlete_DOB date NOT NULL,Athlete_Gender varchar(10) NOT NULL,Country_Code int(11) NOT NULL ,PRIMARY KEY (Athlete_ID))"
    query1= "CREATE TABLE IF NOT EXISTS Result( Athlete_ID int(11) NOT NULL,Medal_Type varchar(30) not null ,Sports_Name varchar(100) not null,PRIMARY KEY(Athlete_ID))"
    query2= "CREATE TABLE IF NOT EXISTS Country( Country_Code int(11) NOT NULL,Country_Name varchar(50) NOT NULL,Primary key(Country_Code))"
    query3= "CREATE TABLE IF NOT EXISTS Schedule(  Athlete_ID int(11) NOT NULL,Date date NOT NULL,Time time NOT NULL,Venue varchar(20) not null,Sports_Name varchar(100) not null,Primary key(Athlete_ID))"
    query5= "CREATE TABLE IF NOT EXISTS Site(Country_Code int(11) NOT NULL,Year int(5) not null,City varchar(20) not null,Season varchar(20) not null)"
    #query6= "alter table Athlete add foreign key(Country_Code) references Country(Country_Code) on update cascade on delete cascade"
    #query7= "alter table Result add foreign key(Athlete_ID) references Athlete(Athlete_ID) on update cascade on delete cascade"
    #query8= "alter table Result  add foreign key(Athlete_ID) references Schedule(Athlete_ID)"
    #query9= "alter table Site add foreign key(Country_Code) references Country(Country_Code) on update cascade on delete cascade"
    cursor.execute(query)
    cursor.execute(query1)
    cursor.execute(query2)
    cursor.execute(query3)
   
    cursor.execute(query5)
    #cursor.execute(query6)
    #cursor.execute(query7)
    #cursor.execute(query8)
    #cursor.execute(query9)

    cursor.close()
    return render_template('index.html')
@app.route('/login',methods=['GET', 'POST'])
def login():
    conn = mysql.connect()
    cursor =conn.cursor()
    query="CREATE TABLE IF NOT EXISTS accounts (id int(11) NOT NULL AUTO_INCREMENT,username varchar(50) NOT NULL,password varchar(255) NOT NULL,email varchar(100) NOT NULL,PRIMARY KEY (id))"
    cursor.execute(query)
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
      
        email = request.form['email']
        password = request.form['password']
    

        cursor.execute('SELECT * FROM accounts WHERE email = %s AND password = %s', (email, password))
       
        account = cursor.fetchone()
        
       
        if account:
            session['loggedin'] = True
            session['id'] = account['email']
            session['username'] = account['password']
            return redirect(url_for('index'))
        else:

            msg = 'Incorrect username/password!'
    
    
    return render_template('login.html',msg=msg)


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form and 'username' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute('SELECT * FROM accounts WHERE email =%s', (email,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email))
            conn.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    
    return render_template('login.html', msg=msg)







@app.route('/team')
def team():
    if 'loggedin' in session:
        return render_template('team.html')
    else:
        return render_template('login.html')

@app.route('/form')
def form():
    if 'loggedin' in session:      
        return render_template('form.html')
    else:
        return redirect(url_for('login'))

@app.route('/post',methods=['GET','POST'])
def post():
    msg=""
    if request.method == 'POST' and 'ID' in request.form and 'fname' in request.form and 'lname' in request.form and 'date1' in request.form and 'gender' in request.form and 'country' in request.form and 'date2' in request.form and 'time' in request.form and 'sname' in request.form and 'cname' in request.form and 'year' in request.form  and 'sportsname' in request.form and 'venue' in request.form and 'mtype' in request.form:
        Athlete_ID=request.form['ID']
        firstname = request.form['fname']
        lastname = request.form['lname']
        date_of_birth = request.form['date1']
        date_of_birth1=date_of_birth.split('/')
        try:
            date_of_birth2=date_of_birth1[2]+"-"+date_of_birth1[0]+"-"+date_of_birth1[1]
        except IndexError:
            pass
        gender=request.form['gender']
        country=request.form['country']
        date_of_event=request.form['date2']
        date_of_event1=date_of_event.split('/')
        try:
            date_of_event2=date_of_event1[2]+"-"+date_of_event1[0]+"-"+date_of_event1[1]
        except IndexError:
            pass
        time_of_event=request.form['time']
        season_name=request.form['sname']
        city_name=request.form['cname']
        year=request.form['year']
        sports_name=request.form['sportsname']
        venue=request.form['venue']
        medal_type=request.form['mtype']
        dict1={'India':1,'Denmark':2,'Pakistan':3,'Japan':4,'Russia':5,'USA':6}
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute('SELECT * FROM Athlete WHERE Athlete_ID =%s',(Athlete_ID,))
        
        athlete = cursor.fetchone()
        
        if athlete:
            msg = 'User Already Exist'
        elif not Athlete_ID or not firstname or not lastname or not date_of_birth or not gender or not country or not date_of_event or not season_name or not city_name or not year or not sports_name or not medal_type or not venue:
            msg = 'Please fill out the form!'
        else:
            country_code=int(dict1[country])
            
            #sql = "INSERT INTO Country (Country_Code,Country_Name) VALUES (%s,%s)"
            #cursor.execute(sql, (country_code,country,))
            
            sql="INSERT INTO Athlete (Athlete_ID,Athlete_FirstName,Athlete_LastName,Athlete_DOB,Athlete_Gender,Country_Code) VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(Athlete_ID,firstname,lastname,date_of_birth2,gender,country_code,))
            sql="INSERT INTO Schedule (Athlete_ID,Date,Time,Venue,Sports_Name) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sql,(Athlete_ID,date_of_event2,time_of_event,venue,sports_name,))
            sql="INSERT INTO Result (Athlete_ID,Medal_Type,Sports_Name) VALUES (%s,%s,%s)"
            cursor.execute(sql,(Athlete_ID,medal_type,sports_name,))
            sql="INSERT INTO Site (Year,Country_Code,City,Season) VALUES (%s,%s,%s,%s)"
            cursor.execute(sql,(year,country_code,city_name,season_name,))
            conn.commit()

            


            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!' 
    return render_template('form.html',msg=msg)
    
@app.route('/view')
def view():
    if 'loggedin' in session:
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute("select * from Athlete")
        Athlete_data=cursor.fetchall()
        cursor.execute("select * from Country")
        Country_data=cursor.fetchall()
        cursor.execute("select * from Result")
        Result_data=cursor.fetchall()
        cursor.execute("select * from Schedule")
        Schedule_data=cursor.fetchall()
        cursor.execute("select * from Site")
        Site_data=cursor.fetchall()
        return render_template('view.html',Athlete_data=Athlete_data,Country_data=Country_data,Result_data=Result_data,Schedule_data=Schedule_data,Site_data=Site_data)
    else:
        return render_template('login.html')
@app.route('/query')
def query():
    if 'loggedin' in session:
        return render_template('queries.html')   
    else:
        return redirect('login')
@app.route('/query/run',methods=['GET','POST'])
def runquery():
    if request.method == 'POST' and 'query' in request.form:
        queries=request.form['query']
        cnx = mysql.connect()
        cursor = cnx.cursor()
        x=int(queries)
        if(x==1):
            queries1="SELECT count(*) FROM  Site WHERE City='Rio'"
            cursor.execute(queries1)
            data=cursor.fetchall()
            n=[]
            for i in data:
                l=list(i.keys())
                m=list(i.values())
                n.append(m)
            c=len(l)
        elif(x==2):
            queries1="select count(distinct Athlete_ID) from athlete inner join site using(Country_Code) where City='Rio' and Athlete_Gender='Male'"
            cursor.execute(queries1)
            data=cursor.fetchall()
            n=[]
            for i in data:
                l=list(i.keys())
                m=list(i.values())
                n.append(m)
            c=len(l)
            
        elif(x==3):
            queries1="select count(Medal_Type) from Result where Medal_Type='Gold'"
            cursor.execute(queries1)
            data=cursor.fetchall()
            n=[]
            for i in data:
                l=list(i.keys())
                m=list(i.values())
                n.append(m)
            c=len(l)
            
        elif(x==4):
            queries1="select CONCAT(Athlete_FirstName ,' ',Athlete_Lastname) AS Athlete_FullName from Athlete inner join Result using(Athlete_ID) where Sports_Name='Wrestling' and Country_Code='1'"
            cursor.execute(queries1)
            data=cursor.fetchall()
            n=[]
            for i in data:
                l=list(i.keys())
                m=list(i.values())
                n.append(m)
            c=len(l)
        
        elif(x==5):
            queries1="select count(*) from Athlete left join Result using(Athlete_ID) where Sports_Name='Badminton' and Country_Code='4' and Athlete_Gender='Female'"
            cursor.execute(queries1)
            data=cursor.fetchall()
            n=[]
            for i in data:
                l=list(i.keys())
                m=list(i.values())
                n.append(m)
            c=len(l)
            
        elif(x==6):
            queries1="SELECT count(*),Country_Name from Athlete left join Country using(Country_Code) GROUP BY Country_Name"
            cursor.execute(queries1)
            data=cursor.fetchall()
            n=[]
            for i in data:
                l=list(i.keys())
                m=list(i.values())
                n.append(m)
            c=len(l)
        elif(x==7):
            queries1="SELECT * from Athlete left join Country using(Country_Code) ORDER BY Country_Name asc"
            cursor.execute(queries1)
            data=cursor.fetchall()
            n=[]
            for i in data:
                l=list(i.keys())
                m=list(i.values())
                n.append(m)
            c=len(l)
        elif(x==8):
            queries1="SELECT * from Athlete left join Country using(Country_Code) ORDER BY Country_Name desc"
            cursor.execute(queries1)
            data=cursor.fetchall()
            n=[]
            for i in data:
                l=list(i.keys())
                m=list(i.values())
                n.append(m)
            c=len(l)
        elif(x==9):
            queries1="SELECT * FROM Athlete WHERE Athlete_DOB >= '1990-01-01' AND Athlete_DOB <= '1995-12-31' ORDER BY Athlete_DOB"
            cursor.execute(queries1)
            data=cursor.fetchall()
            n=[]
            for i in data:
                l=list(i.keys())
                m=list(i.values())
                n.append(m)
            c=len(l)
        elif(x==10):
            queries1="SELECT * FROM Athlete WHERE Athlete_FirstName like 'S%'"
            cursor.execute(queries1)
            data=cursor.fetchall()
            n=[]
            for i in data:
                l=list(i.keys())
                m=list(i.values())
                n.append(m)
            c=len(l)
        elif(x==11):
            queries1="select distinct venue from Schedule,Site where City='Rio'"
            cursor.execute(queries1)
            data=cursor.fetchall()
            n=[]
            for i in data:
                l=list(i.keys())
                m=list(i.values())
                n.append(m)
            c=len(l)
        elif(x==12):
            queries1="select CONCAT(Athlete_FirstName ,' ',Athlete_Lastname) AS Athlete_FullName,Sports_Name from Athlete left join Result using(Athlete_ID) where Medal_Type='Gold'"
            cursor.execute(queries1)
            data=cursor.fetchall()
            n=[]
            for i in data:
                l=list(i.keys())
                m=list(i.values())
                n.append(m)
            c=len(l)
        elif(x==13):
            queries1="select Sports_Name,Athlete_FirstName from Schedule left join Athlete using(Athlete_ID) where Date like '_____08_18' and Time between '12:00:00' and '18:00:00'"
            cursor.execute(queries1)
            data=cursor.fetchall()
            n=[]
            for i in data:
                l=list(i.keys())
                m=list(i.values())
                n.append(m)
            c=len(l)
        elif(x==14):
            queries1="select count(*),Country_Code from Result left join Athlete using(Athlete_ID) where Medal_type !='No Medal'  group by Country_Code"
            cursor.execute(queries1)
            data=cursor.fetchall()
            n=[]
            
            for i in data:
                l=list(i.keys())
                m=list(i.values())
                n.append(m)
            c=len(l)
        elif(x==15):
            queries1="select CONCAT(Athlete_FirstName ,' ',Athlete_Lastname) AS Athlete_FullName from Athlete left join Result using(Athlete_ID) where Athlete_Gender='Female' and Medal_Type='Gold'"
            cursor.execute(queries1)
            data=cursor.fetchall()
            n=[]
            
            for i in data:
                l=list(i.keys())
                m=list(i.values())
                n.append(m)
            c=len(l)
        elif(x==16):
            queries1="select CONCAT(Athlete_FirstName ,' ',Athlete_Lastname) AS Athlete_FullName from Athlete left join Schedule using(Athlete_ID) where venue='Sao paulo'"
            cursor.execute(queries1)
            data=cursor.fetchall()
            n=[]
            
            for i in data:
                l=list(i.keys())
                m=list(i.values())
                n.append(m)
            c=len(l)
        elif(x==17):
            queries1="select distinct Sports_Name from Schedule where venue='Deodoro'"
            cursor.execute(queries1)
            data=cursor.fetchall()
            n=[]
            
            for i in data:
                l=list(i.keys())
                m=list(i.values())
                n.append(m)
            c=len(l)
        elif(x==18):
            queries1="select Athlete_LastName from Athlete where Athlete_LastName like 'M%'"
            cursor.execute(queries1)
            data=cursor.fetchall()
            n=[]
            
            for i in data:
                l=list(i.keys())
                m=list(i.values())
                n.append(m)
            c=len(l)

        elif(x==19):
            queries1="select * from Athlete where Athlete_FirstName like '_a%'"
            cursor.execute(queries1)
            data=cursor.fetchall()
            n=[]
            
            for i in data:
                l=list(i.keys())
                m=list(i.values())
                n.append(m)
            c=len(l)
        elif(x==20):
            queries1="select * from Schedule where venue like 'S%'"
            cursor.execute(queries1)
            data=cursor.fetchall()
            n=[]
            
            for i in data:
                l=list(i.keys())
                m=list(i.values())
                n.append(m)
            c=len(l)
    return render_template('queries.html',data=data,queries1=queries1,l=l,n=n,c=c)
if __name__ == "__main__":
    app.run(debug=True)