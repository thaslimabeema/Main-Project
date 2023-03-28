from flask import *
from database import *
from public import *
import uuid
user=Blueprint('user',__name__)


@user.route('/userhome')
def userhome():
    return render_template('userhome.html')

@user.route('/updateprofile',methods=['post','get'])
def updateprofile():
    data={}
    #session['id'] = id
    s="select * from customers where login_id='%s'"%(session['lid'])
    res=select(s)
    
    data['view']=res

    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
    else:
        action=None
    if action=='update':
       # qry="SELECT * FROM subcategory INNER JOIN category USING(category_id) where subcategory_id='%s'"%(id)
        qry="select * from customers where user_id='%s'"%(id) 
        res1=select(qry)
        data['upd']=res1

    if 'update' in request.form:
        fn=request.form['first_name']
        ln=request.form['last_name']
        hn=request.form['house_name']
        pl=request.form['place']
        pin=request.form['pincode']
        q="update customers set first_name='%s',last_name='%s',house_name='%s',place='%s',pincode='%s' where user_id='%s'"%(fn,ln,hn,pl,pin,id)
        res2=update(q)
        return redirect(url_for('user.updateprofile'))
    return render_template('updateprofile.html',data=data)

"""
@user.route('/addpost',methods=['post','get'])
def addpost():
    data={}
    qry="select * from subcategory"
    res=select(qry)
    data['drop']=res
    w="select user_id from customers where login_id='%s'"%(session['lid'])
    tt=select(w)
    print(tt)
    res3=tt[0]['user_id']
    print("userid",res3)
    if 'submit' in request.form:
        t=request.form['post_title']
        a=request.form['amount']
        s=request.form['subcategory_id']

        q="insert into post_master values(null,'%s','%s',null,'%s',now(),'pending','%s')"%(res3,t,a,s)
        res=insert(q)
        print(res)
        fl=request.files['file']
        path="static/uploads/"+str(uuid.uuid4())+fl.filename
        fl.save(path)
        u="insert into files values(null,'%s','%s','post_file','%s')"%(res3,path,res)
        v=insert(u)

    #s="select * from post_master where user_id='%s'"%(session['lid'])
    s="SELECT *,user_id FROM post_master INNER JOIN subcategory USING (subcategory_id) WHERE user_id='%s'"%(res3)
    res=select(s)
    data['view']=res
    

    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
    else:
        action=None
    if action=='amenity':
        qry="select * from post_master where post_id='%s'"%(id) 
        res1=select(qry)
        data['amenity']=res1

    if 'amenity' in request.form:
       an=request.form['amenity_name']
       q="insert into amenities values(null,'%s')"%(an)      
       res=insert(q)
       print(res)
       return redirect(url_for('user.addpost'))
    
    if action=='description':
        qry="select * from post_master where post_id='%s'"%(id) 
        res1=select(qry)
        data['description']=res1

    if 'description' in request.form:
       ds=request.form['description']
       q="update post_master set description='%s' where post_id='%s'"%(ds,id)      
       res=update(q)
       return redirect(url_for('user.addpost'))
    
    if action=='image':
        qry="select * from post_master where post_id='%s'"%(id) 
        res1=select(qry)
        data['image']=res1

    if 'image' in request.form:
        fl=request.files['file']
        path="static/uploads/"+str(uuid.uuid4())+fl.filename
        fl.save(path)
        u="insert into post_images values(null,'%s','%s')"%(id,path)
        v=insert(u)
        print(u)
        return redirect(url_for('user.addpost'))
    
    return render_template('addpost.html',data=data)
"""

@user.route('/addpost2',methods=['post','get'])
def addpost2():
    data={}
    qry="select * from subcategory"
    res=select(qry)
    data['drop']=res
    w="select user_id from customers where login_id='%s'"%(session['lid'])
    tt=select(w)
    print(tt)
    res3=tt[0]['user_id']
    print("userid",res3)
    if 'submit' in request.form:
        t=request.form['post_title']
        a=request.form['amount']
        s=request.form['subcategory_id']
        ds=request.form['description']
        pl=request.form['place']
        fl=request.files['file']
        path="static/uploads/"+str(uuid.uuid4())+fl.filename
        fl.save(path)

        q="insert into post_master values(null,'%s','%s','%s','%s',now(),'pending','%s','%s')"%(res3,t,ds,a,s,pl)
        res=insert(q)
        print(res)
        
        u="insert into files values(null,'%s','%s','post_file','%s')"%(res3,path,res)
        v=insert(u)
        print(v)

        w="insert into post_images values(null,'%s','%s')"%(res,path)
        x=insert(w)
        print(x)

    #s="select * from post_master where user_id='%s'"%(session['lid'])
    s="SELECT *,user_id FROM post_master INNER JOIN subcategory USING (subcategory_id) WHERE user_id='%s'"%(res3)
    res=select(s)
    data['view']=res

    return render_template('addpost2.html',data=data)

@user.route('/viewuserrequest',methods=['post','get'])
def viewuserrequests():
    data={}
    w="select user_id from customers where login_id='%s'"%(session['lid']) 
    tt=select(w)
    print("user_id=",tt)
    res3=tt[0]['user_id']
    print(res3)
    s="SELECT *,requests.status AS 'request_status',requests.user_id AS 'received_user' FROM requests INNER JOIN post_master USING (post_id) WHERE post_master.user_id='%s'"%(res3)
    res=select(s)
    data['view']=res
    return render_template('viewuserrequest.html',data=data)

@user.route('/user_view_buyer',methods=['get','post'])
def user_view_buyer():
    data={}
    id=request.args['id']
   # w="select * from customers inner join requests using (user_id) "
    w="select user_id from requests where request_id='%s'"%(id)
    res=select(w)
    print(res)
    uid=res[0]['user_id']
    x="select * from customers inner join requests using (user_id) where user_id='%s'"%(uid)
    res1=select(x)
    print(res1)
    data['viewuser']=res1
    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
    else:
        action=None
    if action=='accept':
        q="update requests set status='approved' where request_id='%s'"%(id)
        res=update(q)
        return redirect(url_for('user.user_view_buyer',id=id))
    if action=='reject':
        q="update requests set status='rejected' where request_id='%s'"%(id)
        res=update(q)
        return redirect(url_for('user.user_view_buyer',id=id))
    return render_template('user_view_buyer.html',data=data)

@user.route('/user_view_payment',methods=['post','get'])
def user_view_payment():
    data={}
    id=request.args['id']
    s="select * from payments where request_id='%s'"%(id)
    res=select(s)
    data['view']=res
    return render_template('user_view_payment.html',data=data)

@user.route('/feedback',methods=['post','get'])
def feedback():
    if 'submit' in request.form:
        fb=request.form['feedback']
        q="insert into feedback values(null,now(),'%s','%s')"%(session['lid'],fb)
        res=insert(q)
        print(res)
    return render_template('feedback.html')

@user.route('/userviewsendrequest',methods=['post','get'])
def userviewsendrequest():
    data={}
    w="select user_id from customers where login_id='%s'"%(session['lid']) 
    tt=select(w)
    print(tt)
    res3=tt[0]['user_id']
    s="SELECT *,requests.status AS 'request_status' FROM requests INNER JOIN post_master USING (post_id) where requests.user_id='%s'"%(res3)
    print(session['lid'])
    res=select(s)
    data['view']=res
    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
    else:
        action=None
    if action=='unsent':
        q="delete from requests where request_id='%s'"%(id)
        delete(q)
        return redirect(url_for('user.userviewsendrequest'))  
    return render_template('userviewsendrequest.html',data=data)

@user.route('/viewothersposts',methods=['post','get'])
def viewothersposts():
    data={}
    #######################################################
    #----userid-----------------
    print("sessionid aka login id",session['lid'])
    w="select user_id from customers where login_id='%s'"%(session['lid']) 
    tt=select(w)
    print(tt)
    res3=tt[0]['user_id']
    print("user_id",res3)
    ##########################################################

    #s="SELECT *,post_master.user_id,post_master.status AS 'post_status' FROM post_master INNER JOIN post_images USING(post_id) INNER JOIN requests USING(post_id) WHERE post_master.status='Approved' and post_master.user_id!='%s'"%(res3)
    s="SELECT *,post_master.user_id,post_master.status AS 'post_status' FROM post_master INNER JOIN post_images USING(post_id) WHERE post_master.status='Approved' and post_master.user_id!='%s'"%(res3)
    res=select(s)
    data['view']=res

    qry="select * from category"
    res=select(qry)
    data['drop']=res

    qry9="select * from subcategory"
    res9=select(qry9)
    data['drop2']=res9

    print("sessionid aka login id",session['lid'])
    w="select user_id from customers where login_id='%s'"%(session['lid']) 
    tt=select(w)
    print(tt)
    res3=tt[0]['user_id']

    if 'search' in request.form:
        qry="select * from category"
        res=select(qry)
        data['drop']=res
        print(res)
        ci=request.form['category_id']
        print("category id ",ci)

        qry9="select * from subcategory where category_id='%s'"%(ci)
        res9=select(qry9)
        data['drop2']=res9
        si=request.form['subcategory_id']
        print("subcategory id ",si)

        qry3="SELECT *,post_master.user_id,post_master.status AS 'post_status' FROM post_master INNER JOIN post_images USING(post_id) INNER JOIN requests USING(post_id) inner join subcategory using (subcategory_id) WHERE subcategory.subcategory_id='%s' AND subcategory.category_id='%s' AND post_master.user_id!='%s'"%(si,ci,res3)
        res8=select(qry3)
        data['view2']=res8

    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
    else:
        action=None
    if action=='sendrequest':
        #q="update requests set status='request to buy' where post_id='%s'"%(id)
        q="insert into requests values(null,'%s','%s','request to buy',now())"%(res3,id)
        print(id)
        res=insert(q)
        return redirect(url_for('user.viewothersposts'))
    return render_template('viewothersposts.html',data=data)

@user.route('/userviewimages',methods=['get','post'])
def userviewimages():
    data={}
    id=request.args['id']
    print(id)
    s="select post_id from post_master where post_id='%s'"%(id)
    res1=select(s)
    print(res1)
    pid=res1[0]['post_id']
    print("postid",pid)
    w="select * from `post_master` inner join files using (post_id) where post_id='%s'"%(pid)
    res=select(w)
    data['view']=res
    
    return render_template('userviewimages.html',data=data)

@user.route('/paymentconfirmation',methods=['post','get'])
def paymentconfirmation():
    data={}
    id=request.args['id']
    print("postid=",id)
    s="SELECT * from payments inner join requests using(request_id)"
    res=select(s)
    data['view']=res
    w="select request_id from requests where post_id='%s'"%(id)
    tt=select(w)
    print(tt)
    res3=tt[0]['request_id']
    if 'submit' in request.form:
        q="update payments set payment_status='completed' where request_id='%s'"%(res3)
        res1=update(q)
        return redirect(url_for('user.paymentconfirmation',id=id))
    return render_template('paymentconfirmation.html',data=data)


    

    

