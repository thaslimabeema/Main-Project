from flask import *
from database import *
admin=Blueprint('admin',__name__)

@admin.route('/adminhome')
def adminhome():
    return render_template('adminhome.html')

@admin.route('/logout')
def logout():
    return render_template('logout.html')

@admin.route('/viewcustomers')
def viewcustomers():
    data={}
    s="select * from customers inner join login using (login_id)"
    res=select(s)
    data['view']=res

    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
    else:
        action=None
    
    if action=='delete':
        w="select login_id from customers where user_id='%s'"%(id)
        res=select(w)
        y=res[0]['login_id']
        r="delete from login where login_id='%s'"%(y)
        delete(r)
        q= "delete from customers where user_id='%s'"%(id)
        delete(q)
        print("deleted")
        return redirect(url_for('admin.viewcustomers'))   
    return render_template('viewcustomers.html',data=data)

@admin.route('/admin_view_files',methods=['get','post'])
def admin_view_files():
    data={}
    id=request.args['id']
    w="select * from login inner join `customers` using(login_id) inner join files using (user_id) where usertype='pending' and user_id='%s'"%(id)
    res=select(w)
    print(res)
    data['view']=res
    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
    else:
        action=None
    if action=='accept':
        q="update login set usertype='User' where login_id='%s'"%(id)
        res=update(q)
        return redirect(url_for('admin.viewcustomers'))
    if action=='reject':
        q="update login set usertype='rejected' where login_id='%s'"%(id)
        res=update(q)
        return redirect(url_for('admin.viewcustomers'))
    return render_template('admin_view_files.html',data=data)

@admin.route('/admin_view_files2',methods=['get','post'])
def admin_view_files2():
    data={}
    id=request.args['id']
    print(id)
    s="select post_id from post_master where user_id='%s'"%(id)
    res1=select(s)
    pid=res1[0]['post_id']
    w="select * from `post_master` inner join files using (post_id) where post_id='%s'"%(pid)
    res=select(w)
    data['view']=res
    
    return render_template('admin_view_files2.html',data=data)

@admin.route('/managecategory',methods=['post','get'])
def managecategory():
    data={}
    if 'submit' in request.form:
        cn=request.form['category_name']
        q="insert into category values(null,'%s')"%(cn)
        res=insert(q)
        return redirect(url_for('admin.managecategory'))
        print(res)

    r="select * from category"
    re=select(r)
    data['view']=re

    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
    else:
        action=None
    if action=='update':
        qry="select * from category where category_id='%s'"%(id) 
        res1=select(qry)
        data['upd']=res1

    if 'update' in request.form:
        cn=request.form['category_name']
        q="update category set category_name='%s' where category_id='%s'"%(cn,id)
        res=update(q)
        return redirect(url_for('admin.managecategory'))
    
    if action=='delete':
        qry="select * from category where category_id='%s'"%(id) 
        res2=select(qry)
        data['del']=res2

    if 'delete' in request.form:
        q= "delete from category where category_id='%s'"%(id)
        res=delete(q)
        return redirect(url_for('admin.managecategory'))

    return render_template('managecategory.html',data=data)

@admin.route('/managesubcategory',methods=['post','get'])
def managesubcategory():
    data={}
    qry="select * from category"
    res=select(qry)
    data['drop']=res

    if 'submit' in request.form:
        sn=request.form['subcategory_name']
        ci=request.form['category_id']
        print(res)
        #ci=res[0]['category_id']
        print(ci)
        q="insert into subcategory values(null,'%s','%s')"%(ci,sn)
        res=insert(q)
        return redirect(url_for('admin.managesubcategory'))
        print(res)

    r="SELECT * FROM subcategory INNER JOIN category USING(category_id)"
    re=select(r)
    data['view']=re

    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
    else:
        action=None
    if action=='update':
       # qry="SELECT * FROM subcategory INNER JOIN category USING(category_id) where subcategory_id='%s'"%(id)
        qry="select * from subcategory inner join category using (category_id) where subcategory_id='%s'"%(id) 
        res1=select(qry)
        print(re)
        data['upd']=res1

    if 'update' in request.form:
        cn=request.form['subcategory_name']
        cid=request.form['category_id']
        q="update subcategory set subcategory_name='%s',category_id='%s' where subcategory_id='%s'"%(cn,cid,id)
        res=update(q)
        return redirect(url_for('admin.managesubcategory'))
    
    if action=='delete':
        qry="select * from subcategory where subcategory_id='%s'"%(id) 
        res2=select(qry)
        data['del']=res2

    if 'delete' in request.form:
        q= "delete from subcategory where subcategory_id='%s'"%(id)
        res=delete(q)
        return redirect(url_for('admin.managesubcategory'))
    return render_template('managesubcategory.html',data=data)

@admin.route('/manageposts')
def manageposts():
    data={}
   # s="select * from post_master"
    s="SELECT * FROM post_master INNER JOIN customers USING(user_id) INNER JOIN subcategory USING (subcategory_id)"
    res=select(s)
    data['view']=res
    
    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
    else:
        action=None
    
    if action=='remove':
        #qry="select * from category where category_id='%s'"%(id) 
        #res2=select(qry)
        #data['del']=res2
        q= "delete from post_master where post_id='%s'"%(id)
        delete(q)
        print("deleted")
        return redirect(url_for('admin.manageposts'))
    
    if action=='approve':
        r="update post_master set status='Approved' where post_id='%s'"%(id)
        update(r)
        print('updated')
        return redirect(url_for('admin.manageposts'))
    
    if action=='reject':
        r="update post_master set status='rejected' where post_id='%s'"%(id)
        update(r)
        print('updated')
        return redirect(url_for('admin.manageposts'))

    return render_template('manageposts.html',data=data)

@admin.route('/viewfeedback')
def viewfeedback():
    data={}
    s="select * from customers INNER JOIN feedback using(user_id)"
    res=select(s)
    data['view']=res
    #return redirect(url_for('admin.viewfeedback'))
    return render_template('viewfeedback.html',data=data)

@admin.route('/viewrequests')
def viewrequests():
    data={}
    s="select * from requests"
    res=select(s)
    data['view']=res
    return render_template('viewrequests.html',data=data)



    

  

   

