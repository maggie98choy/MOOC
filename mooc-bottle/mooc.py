from bottle import route,run,request,response,template,redirect,view
import storage
from bson.json_util import dumps
import json
import ConfigParser


@route('/category', method="POST")
def add_category():
	name=request.forms.get('name')
	descr=request.forms.get('description')
	createdate=request.forms.get('createDate')
	status=request.forms.get('status')

	categories=({'name':name,'description':descr,'createDate':createdate,'status':status})

	storage.addcategory(categories)
	response.status=201
	cat1= {'name':name,'description':descr,'createDate':createdate,'status':status,"id":str(categories['_id'])}
	return {'success':True,'category':cat1}
	

@route('/course', method="POST")
def add_course():
	cat=request.forms.get('category')
	title=request.forms.get('title')
	section=request.forms.get('section')
	dept=request.forms.get('dept')
	term=request.forms.get('term')
	year=request.forms.get('year')
	instructor=request.forms.get('instructor')
	days=request.forms.get('days')
	hours=request.forms.get('hours')
	descr=request.forms.get('Description')
	attach=request.forms.get('attachment')
	version=request.forms.get('version')

	courses={"category":cat,"title":title,"section":section,"dept":dept,"term":term,"year":year,"instructor":instructor,"days":days,"hours":hours,"Description":descr,"attachment":attach,"version":version}

	storage.addcourse(courses)

	response.status=201
	cou1 = {"category":cat,"title":title,"section":section,"dept":dept,"term":term,"year":year,"instructor":instructor,"days":days,"hours":hours,"Description":descr,"attachment":attach,"version":version,"id":str(courses['_id'])} 

	return {"success":True,'course':cou1}


@route('/category/:id', method="GET")
def get_category(id):
	cid=request.query["id"]
	res=storage.getcategory(cid)
	if res==0:
		response.status=400
		return{"success":False}
	else:
		result=json.loads(res)
		name= result['name']
		descr=result['description']
		creDate=result['createDate']
		status=result['status']
		cat1= {"name":name,"description":descr,"createDate":creDate,"status":status,"id":cid}
		return {"success":True,"category":cat1}



@route('/course/:id', method="GET")
def get_course(id):
	cid=request.query["id"]
	res=storage.getcourse(cid)
	if res==0:
		response.status=400
		return {"success":False}
	else:
		result=json.loads(res)
		print result
		cat= result["category"]
		title=result['title']
		section=result['section']
		dept=result['dept']
		term=result['term']
		year=result['year']
		instructor=result['instructor']
		days=result['days']
		hours=result['hours']
		descr=result['Description']
		attach=result['attachment']
		version=result['version']
		cid=str(result['_id'])
		cou1= {"category":cat,"title":title,"section":section,"dept":dept,"term":term,"year":year,"instructor":instructor,"days":days,"hours":hours,"Description":descr,"attachment":attach,"version":version,"id":cid}

		return {"success":True,"course":cou1}

		
@route('/category/list',method="GET")
def list_category():
	result=storage.listcategory()
	return {result}
	
@route('/course/list',method="GET")
def list_course():
	result=storage.listcourse()
	return {result}
	
	
#@view('base')	
#@route('/course/list', method="GET")
#def list_course():
#	result= storage.listcourse()
#	clist=json.loads(result)
#	print clist
#	course_List=[]
#	for row in clist:
#		id_list=row
#		course_List+=[{"category":id_list['category'],"title":id_list['title'],"section":id_list['section'],"dept":id_list['dept'],"term":id_list['term'],"year":id_list['year'],"instructor":id_list['instructor'],"days":id_list['days'],"hours":id_list['hours'],"Description":id_list['Description'],"attachment":id_list['attachment'],"version":id_list['version']}]
	
#	tpl=SimpleTemplate('base', CourseList=course_List)
#	tpl.render()
#	redirect("/base")
#	response.status=303
#	return template('base',CourseList=course_List)

#@route('/base')
#def list():
#	return '''<html>
#<title>List of courses</title>
#<body>
#<br/><br/>

#<table border="1">
       # <tr>
        #        <td>Category</td><td>Title</td><Section</td><td>Department</td><td>Term</td><td><Year</td><td>Instructor</td><td><Days></td><td>Hours</td><td>Description</td><td>Attachment</td><td>Version</td>
       # </tr>

       # {% for i in CourseList %}
       # <tr>
        #        <td>{{i.category}}</td> <td>{{i.title}}</td> <td>{{i.section}}</td> <td>{{i.dept}}</td>
#<td>{{i.term}}</td> <td><{{i.year}}</td> <td>{{i.instructor}}</td> <td>{{i.days}}</td> <td>{{i.hours}}</td> <td>{{i.Description}}</td> <td>{{i.attachment}}</td> <td>{{i.version}}</td>
 #       </tr>
#</table>
#</body>
#</html>'''


@route('/course/update/:id', method="PUT")
def update_course(id):
	cid=request.query["id"]

	cat=request.forms.get('category')
        title=request.forms.get('title')
        section=request.forms.get('section')
        dept=request.forms.get('dept')
        term=request.forms.get('term')
        year=request.forms.get('year')
        instructor=request.forms.get('instructor')
        days=request.forms.get('days')
        hours=request.forms.get('hours')
        descr=request.forms.get('Description')
        attach=request.forms.get('attachment')
        version=request.forms.get('version')

	
	courses={"category":cat,"title":title,"section":section,"dept":dept,"term":term,"year":year,"instructor":instructor,"days":days,"hours":hours,"Description":descr,"attachment":attach,"version":version}

	
	result=storage.updatecourse(cid,courses)
	if result==0:
		response.status=404
		return {"success":False}
	else:
		cou1= {"category":cat,"title":title,"section":section,"dept":dept,"term":term,"year":year,"instructor":instructor,"days":days,"hours":hours,"Description":descr,"attachment":attach,"version":version,"id":cid}

		return{"success":True,"course":cou1}
	
@route('/course/:id', method="DELETE")
def delete_course(id):
	cid=request.query["id"]
	result=storage.deletecourse(cid)
	if result==0:
		response.status=404
		return{"success":False},
	else:
		return{"success":True,"courseId":cid}

@route('/course/enroll', method="PUT")
def enroll_course():
	uid=request.forms.get("email")
	cid=request.forms.get("courseid")
	
	result=storage.enrollcourse(cid,uid) 
	return {"success":True,"courseId":cid}

@route('/course/drop', method= "PUT")
def unenroll_course():
	uid= request.forms.get("email")
	cid=request.forms.get("courseid")

	result=storage.unenrollcourse(cid,uid)
	return{"success":True,"courseId":cid}

@route('/announcement', method="POST")
def add_announcement():
	courseid=request.forms.get('courseid')
	title=request.forms.get('title')
	description=request.forms.get('description')
	postDate=request.forms.get('postDate')
	status=request.forms.get('status')
	print 'asddf==', courseid
	announcements={"courseid":courseid,"title":title,"description":description,"postDate":postDate,"status":status}
	
	storage.addannouncement(announcements)
	
	response.status=201 
	return {"success":True, "announcement":{"courseid":courseid,"title":title,"description":description,"postDate":postDate,"status":status},"id":str(announcements['_id'])}


	
@route('/announcement/list',method="GET")
def list_announcement():
	result=storage.listannouncement()
	return result

@route('/announcement/update/:id', method="PUT")
def update_announcement(id):
	aid=request.query["id"]
        title=request.forms.get('title')
        descr=request.forms.get('description')
        postDate=request.forms.get('postDate')
        status=request.forms.get('status')
	courseid = request.forms.get('courseid');

	
	announcements={"title":title,"description":descr,"postDate":postDate,"status":status,"courseid":courseid}

	
	result=storage.updateannouncement(aid,announcements)
	if result==0:
		response.status=404
		return {"success":False}
	else:
		return{"title":title,"description":descr,"postDate":postDate,"status":status,"id":aid,"courseid":courseid}
	
	
@route('/announcement/:id', method="DELETE")
def delete_announcement(id):
	aid=request.query["id"]
	
	result=storage.deleteannouncement(aid)
	if result==0:
		response.status=404
		return{"success":False}
	else:
		return{"success":True}


@route('/announcement/:id', method="GET")
def get_announcement(id):
	aid=request.query["id"]
	res=storage.getannouncement(aid)
	if res==0:
		response.status=400
		return {"success":False}
	else:
		result=json.loads(res)
		print result
		courseid= result["courseid"]
		title=result['title']
		description=result['description']
		postDate=result['postDate']
		status=result['status']
		aid=str(result['_id'])
		return{"courseid":courseid,"title":title,"description":description,"postDate":postDate,"status":status,"id":aid}
		

	
config = ConfigParser.ConfigParser()
config.read('moo.ini')
host = config.get("bottle","host")
port = config.get("bottle","port")

print 'host:'+host
print 'port:'+port
run(host=host,port=port)		
run(host=host,port=port)	

