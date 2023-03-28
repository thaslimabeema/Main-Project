from flask import *
from database import *
import uuid
public=Blueprint('public',__name__)

@public.route('/')
def welcome():
    return render_template('welcome.html')

@public.route('/registration',methods=['post','get'])
def registration():
    if 'submit' in request.form:
        fn=request.form['first_name']
        ln=request.form['last_name']
        hn=request.form['house_name']
        pl=request.form['place']
        pin=request.form['pincode']
        ph=request.form['phone']
        em=request.form['email']
        ad=request.form['aadhar']
       # un=request.form['uname']
        #pwd=request.form['password']
        q="insert into login values(null,'%s','%s','pending')"%(em,ph)
        res=insert(q)
        print(res)
        s="insert into customers values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(res,fn,ln,hn,pl,pin,ph,em,ad)
        t=insert(s)
        print(t)
        fl=request.files['file']
        path="static/uploads/"+str(uuid.uuid4())+fl.filename
        fl.save(path)
        u="insert into files values(null,'%s','%s','user_file','NA')"%(t,path)
        v=insert(u)
        print(u)
    return render_template('registration.html')

@public.route('/login',methods=['post','get'])
def login():
    if 'login' in request.form:
        un=request.form['username']
        pwd=request.form['password']
        print(un,pwd)
        q="select * from login where username='%s' and password='%s'"%(un,pwd)
        res=select(q)
        
        print(session['lid'])
        if res:
            session['lid']=res[0]['login_id'] 
            if res[0]['usertype']=='admin':
                return redirect(url_for('admin.adminhome'))
            elif res[0]['usertype']=='User':
                q1="select * from customers where login_id='%s'"%(session['lid'])
                res1=select(q1)
                session['uid']=res1[0]['user_id']
                return redirect(url_for('user.updateprofile'))
        else:
            return'''<script>alert('Invalid Username/Password or your account is not activated yet');window.location='login'</script>'''
    return render_template('login.html')