#from django.http import HttpResponse
from django.shortcuts import render , render_to_response
from django.template import loader, Context, RequestContext
from django.contrib.auth import authenticate, login as auth_login, logout
import json
from django.core.exceptions import ValidationError
from models import CategoryForm, CourseForm, AnnouncementForm
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
import urllib2 
import urllib
import ConfigParser
import string
import datetime


def login(request):
    params ={'':''}    

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                
                template = 'welcome.html'
            else:
                params = {'result':'Account disabled, contact Administrator!'}
                template = 'login.html'
        else:
            params = {'result':'Invalid login!'}
            template = 'login.html'
    else:
        template = 'login.html'        
        
      
    return render_to_response(template, params, context_instance=RequestContext(request))


def displayCategoryForm(request): 
    template = 'category/category.html'
    params ={'':''}
    return render_to_response(template, params, context_instance=RequestContext(request))



def addCategory(request):
    config = ConfigParser.ConfigParser()
    config.read('moo.ini')
			    
    host = config.get("bottle","host")
    port = config.get("bottle","port")
    
    template = 'welcome.html'
    params = {'':''}
    
    if request.method == 'POST':
	form = CategoryForm(request.POST)		
	title = request.POST['title']	   
	
	if form.is_valid():
	    title = request.POST['title']	   
	    
	    print 'Category added.'
	    url='http://'+host+':'+port+'/category'
	    name = request.POST['name']
	    description = request.POST['description']
	    now = datetime.datetime.now()
	    createDate = now.month,'-',now.day,'-',now.year
	    status = '0'
	    method = 'POST'
			
	    args = {'name':name, 'description':description,
	 	        'createDate':createDate,'status':status}
	    encoded_args = urllib.urlencode(args)
	    request = urllib2.Request(url,encoded_args)
	    request.get_method = lambda: method
		
	    try: 
		response = urllib2.urlopen(request)	
		template = 'welcome.html'
		r=response.read()
		result=json.loads(r)
		cid = result['category']['id']
		
		params = {'result':'Category is added succesfully! Category id:'+cid}
				
	    except urllib2.HTTPError, e:
		if(e.code == 409):				 
		    template = 'category/category.html'
		    params = {'result':'Category Name is duplicated'}
		else:
		    template = 'category/category.html'
		    params = {'result':'Server error, try later'}
	else:
	    print 'Invalid form entered. Populate data on form.'
	    name = request.POST['name']
	    description = request.POST['description']
	    print name, description
	    params = {'name':name, 'description':description,'result':'Required  fields are not entered'}
	    template = 'category/category.html'
	                       
    return render_to_response(template, params, context_instance=RequestContext(request))
    

def displayCategorySearchForm(request):
    template = 'category/categorySearchForm.html'
    params ={'':''}
       
    return render_to_response(template, params, context_instance=RequestContext(request))    


def displayEnrollForm(request):
    template = 'course/courseEnrollForm.html'
    params ={'':''}
       
    return render_to_response(template, params, context_instance=RequestContext(request))   



def displayDropForm(request):
    template = 'course/courseDropForm.html'
    params ={'':''}
       
    return render_to_response(template, params, context_instance=RequestContext(request))   



def enrollCourse(request):

    config = ConfigParser.ConfigParser()
    config.read('moo.ini')
				
    host = config.get("bottle","host")
    port = config.get("bottle","port")
	
    template = 'welcome.html'
    params = {'':''}
	
    if request.method == 'POST':
	
	print 'enroll course.'	
	courseid = request.POST['courseid']
	email = request.POST['useremail']
	if len(courseid) > 0:
	    
	    url='http://'+host+':'+port+'/course/enroll'
	    print 'enroll course URL: ',url
	    method = 'PUT'
	    args = {'email':email, 'courseid':courseid}
	    encoded_args = urllib.urlencode(args)
	    
	    request = urllib2.Request(url,encoded_args)
	    request.get_method = lambda: method
		    
	    try: 
		response = urllib2.urlopen(request)	
		r=response.read()
		result =json.loads(r)
		
		print result
		template = 'welcome.html'
				    
	    except urllib2.HTTPError, e:
		template = 'welcome.html'
		params = {'result':'Server error, try again later.'}		
	else:
	    template = 'course/courseEnrollForm.html'
	    params = {'result':'Enter course id!'}

    return render_to_response(template, params, context_instance=RequestContext(request))




def dropCourse(request):

    config = ConfigParser.ConfigParser()
    config.read('moo.ini')
				
    host = config.get("bottle","host")
    port = config.get("bottle","port")
	
    template = 'welcome.html'
    params = {'':''}
	
    if request.method == 'POST':
	
	print 'enroll course.'	
	courseid = request.POST['courseid']
	email = request.POST['useremail']
	if len(courseid) > 0:
	    
	    url='http://'+host+':'+port+'/course/drop'
	    print 'drop course URL: ',url
	    method = 'PUT'
	    args = {'email':email, 'courseid':courseid}
	    encoded_args = urllib.urlencode(args)
	    
	    request = urllib2.Request(url,encoded_args)
	    request.get_method = lambda: method
		    
	    try: 
		response = urllib2.urlopen(request)	
		r=response.read()
		result =json.loads(r)
		
		print result
		template = 'welcome.html'
				    
	    except urllib2.HTTPError, e:
		template = 'welcome.html'
		params = {'result':'Server error, try again later.'}		
	else:
	    template = 'course/courseDropForm.html'
	    params = {'result':'Enter course id!'}

    return render_to_response(template, params, context_instance=RequestContext(request))


    
def searchCategory(request):
    config = ConfigParser.ConfigParser()
    config.read('moo.ini')
				
    host = config.get("bottle","host")
    port = config.get("bottle","port")
	
    template = 'welcome.html'
    params = {'':''}
	
    if request.method == 'POST':
	form = CategoryForm(request.POST)		

	print 'Search category.'	
	categoryid = request.POST['categoryid']
	if len(categoryid) > 0:
	    args = {'id':categoryid}
	    encoded_args = urllib.urlencode(args)
	    url='http://'+host+':'+port+'/category/id?' + encoded_args
	    print 'search category URL: ',url
	    method = 'GET'
	    request = urllib2.Request(url,'')
	    request.get_method = lambda: method
		    
	    try: 
		response = urllib2.urlopen(request)	
		r=response.read()
		result =json.loads(r)
		print result
		params = {'id':result['id'], 'name': result['name'], 
		          'description': result['description']}
		#params = {'id':'1112', 'name': 'Cat1', 
		#              'description': 'descfff'}
		
		template='category/displayCategory.html'
				    
	    except urllib2.HTTPError, e:
		if(e.code == 400):				 
		    template = 'welcome.html'
		    params = {'result':'ID is invalid.'}
		elif(e.code == 404):
		    template = 'welcome.html'
		    params = {'result':'Category not found.'}
		elif(e.code == 500):
		    template = 'welcome.html'
		    params = {'result':'Server error, try again later.'}		
	else:
	    template = 'category/categorySearchForm.html'
	    params = {'result':'Enter category id!'}

    return render_to_response(template, params, context_instance=RequestContext(request))

	
def listCategory(request):    
    config = ConfigParser.ConfigParser()
    config.read('moo.ini')
				   
    host = config.get("bottle","host")
    port = config.get("bottle","port")
    template = 'welcome.html'
    params = {'':''}

    url='http://'+host+':'+port+'/category/list'
    print 'list category URL: ',url
    method = 'GET'
    request = urllib2.Request(url,'')
    request.get_method = lambda: method
			
    try: 
	response = urllib2.urlopen(request)	
	c = response.read()
	clist=json.loads(c)
	print clist
	
	#Category_list = [{"id":"id1","name":"name1", "description":
	#                  "description1"}, {"id":"id2","name":"name1", #"description":"description1"}, {"id":"id3","name":"name1", #"description":"description1"},{"id":"id4","name":"name1", #"description":"description1"}]
	
	Category_list=[]
	for row in clist:
	    id_list=row
	    cid=id_list['_id']
	    Category_list+=[{"id":cid['$oid'], "name": id_list['name'],"description": id_list['description']}]
	
	template='category/viewCategoryList.html'
	CategoryList= Category_list
	params={'CategoryList':CategoryList}	
	
    except urllib2.HTTPError, e:
	if(e.code == 500):				 
	    template = 'welcome.html'
	    params = {'result':'Server error, try again later.'}	   
	
    return render_to_response(template, params, context_instance=RequestContext(request))
 
 
def displayCourseForm(request):
     template = 'course/course.html'
     params ={'':''}
     
     return render_to_response(template, params, context_instance=RequestContext(request))     


def addCourse(request):
    config = ConfigParser.ConfigParser()
    config.read('moo.ini')
				
    host = config.get("bottle","host")
    port = config.get("bottle","port")
	
    template = 'welcome.html'
    params = {'':''}
	
    if request.method == 'POST':
	form = CourseForm(request.POST)		
		
	if form.is_valid():
	    categoryid = request.POST['categoryid']
	    courseid = request.POST['courseid']
	    title = request.POST['title']
	    section = request.POST['section']
	    department = request.POST['department']
	    term = request.POST['term']
	    year = request.POST['year']
	    instructorname = request.POST['instructorname']
	    instructoremail = request.POST['instructoremail']
	    description= request.POST['description']
	    hours = request.POST['hours']
	    #attachment = request.POST['attachment']	
	    version = request.POST['version']	
	
	    #new course -courseid = 0
	    #update course - courseid !=0
	    
	    if courseid =='0':
		url='http://'+host+':'+port+'/course'
		method = 'POST'
	    else:
		args = {'id':courseid}
		encoded_args = urllib.urlencode(args)
		url='http://'+host+':'+port+'/course/update/id?' + encoded_args
		method = 'PUT'			

	    args = {'title':title, 'section':section,'year':year,'instructor':[{'name':instructorname,'email':instructoremail}],'hours':hours,'dept':department,'term':term,'Description':description,'version':version,'category':categoryid,'attachment':'','day':'','hours':''}

	    encoded_args = urllib.urlencode(args)
	    request = urllib2.Request(url,encoded_args)
	    request.get_method = lambda: method
			   
			
	    try: 
		response = urllib2.urlopen(request)	
		r=response.read()
		template = 'welcome.html'
		result=json.loads(r)
		cid = result['course']['id']
		
		params = {'result':'Course is added/updated succesfully! Course id:'+cid}
					
	    except urllib2.HTTPError, e:
		template = 'course/course.html'
		params = {'result':'Server error, try later'}
		
	else:
	    print 'Invalid form entered. Populate data on form.'
	    title = request.POST['title']
	    section = request.POST['section']
	    department = request.POST['department']
	    term = request.POST['term']
	    year = request.POST['year']
	    instructorname = request.POST['instructorname']
	    instructoremail = request.POST['instructoremail']
	    hours = request.POST['hours']
	    description = request.POST['description']
	    version = request.POST['version']
	    categoryid = request.POST['categoryid']
	    
	    params = {'title':title, 'section':section,'department':department,'term':term,'year':year,'instructor':[{'name':instructorname,'email':instructoremail}],'hours':hours, 'description':description,'version':version, 'result':'Required  fields are not entered','category':categoryid}
	    template = 'course/course.html'
				   
    return render_to_response(template, params, context_instance=RequestContext(request))    
  		
  		
def displayCourseSearchForm(request):
    template = 'course/courseSearchForm.html'
    params ={'':''}
       
    return render_to_response(template, params, context_instance=RequestContext(request))    



def searchCourse(request):
    config = ConfigParser.ConfigParser()
    config.read('moo.ini')
				
    host = config.get("bottle","host")
    port = config.get("bottle","port")
	
    template = 'welcome.html'
    params = {'':''}
	
    if request.method == 'POST':
	
	print 'Search course.'	
	courseid = request.POST['courseid']
	if len(courseid) > 0:
	    args = {'id':courseid}
	    encoded_args = urllib.urlencode(args)
	    url='http://'+host+':'+port+'/course/id?' + encoded_args
	    print 'search course URL: ',url
	    method = 'GET'
	    request = urllib2.Request(url,'')
	    request.get_method = lambda: method
		    
	    try: 
		response = urllib2.urlopen(request)	
		r=response.read()
		result =json.loads(r)
		print result

		category= result['course']['category']		
		title= result['course']['title']
		section=result['course']['section']
		department=result['course']['dept']
		term=result['course']['term']
		year=result['course']['year']
		hours=result['course']['hours']
		descp=result['course']['Description']
		version=result['course']['version']
		inst=result['course']['instructor']	
	
		instr=inst[12:]
		count=0
		for r in instr:	
			count=count+1
			if(r==':'):
				emailstart=count+3
				break

			
		inst_name=inst[12:emailstart-2]
		inst_email=instr[emailstart:-3]
		
	
		params = {'categoryid':category, 'title':title,'section': section,'department': department,'term': term,'year': year,'instructorname': inst_name,'instructoremail':inst_email,'hours': hours,'description': descp,'version': version,'courseid':courseid}
		
		#params = {'id':'id1', 'title': 'title1', 
		#  'section': 'section1','department': 'depart1','term': 'term1','year': 'year1','instructorname': 'instructorname1','instructoremail':'instructoremail1','hours': 'hours1','description': 'description1','version': 'version1'}
		
		
		
		template = 'course/displayCourse.html'
				    
	    except urllib2.HTTPError, e:
		if(e.code == 400):				 
		    template = 'welcome.html'
		    params = {'result':'ID is invalid.'}
		elif(e.code == 404):
		    template = 'welcome.html'
		    params = {'result':'Course not found.'}
		elif(e.code == 500):
		    template = 'welcome.html'
		    params = {'result':'Server error, try again later.'}		
	else:
	    template = 'course/courseSearchForm.html'
	    params = {'result':'Enter course id!'}

    return render_to_response(template, params, context_instance=RequestContext(request))


def listCourse(request):  
    config = ConfigParser.ConfigParser()
    config.read('moo.ini')
				   
    host = config.get("bottle","host")
    port = config.get("bottle","port")
    template = 'welcome.html'
    params = {'':''}

    url='http://'+host+':'+port+'/course/list'
    print 'list category URL: ',url
    method = 'GET'
    request = urllib2.Request(url,'')
    request.get_method = lambda: method
			
    try: 
	response = urllib2.urlopen(request)	
	c = response.read()
        clist=json.loads(c)
        print clist

	#redirect page occur here	
#	redirecturl = response.geturl()
	
	#clist=json.loads(c)
	#print clist
	
	#Course_list = [{"id":"id1","title":"title1", "section":
	#                  "section1"}, {"id":"id2","title":"title11", "section":"section1"}, {"id":"id3","title":"title3", "section":"section3"},{"id":"id4","title":"title4", "section":"section4"}]
	
	Course_list=[]
	for row in clist:
		id_list=row
		cid=id_list['_id']
	   # instr=id_list['instructor']
		inst=id_list['instructor']
		instr=inst[12:]
                count=0
                for r in instr:
                        count=count+1
                        if(r==':'):
                                emailstart=count+3
                                break


                inst_name=inst[12:emailstart-2]
                inst_email=instr[emailstart:-3]

		Course_list+=[{"categoryid":id_list['category'], "title": id_list['title'],"section": id_list['section'],"year":id_list['year'],"instructorname": inst_name,"instructoremail": inst_email,"hours": id_list['hours'],"department": id_list['dept'],"term": id_list['term'],"description": id_list['Description'],"version": id_list['version']}]
    
	template='course/viewCourseList.html'
	CourseList= Course_list
	params={'CourseList':CourseList}	
	
    except urllib2.HTTPError, e:
	if(e.code == 500):				 
	    template = 'welcome.html'
	    params = {'result':'Server error, try again later.'}	   
	
    return render_to_response(template, params, context_instance=RequestContext(request))
     

def displayCourseDeleteForm(request):
    template = 'course/courseDeleteForm.html'
    params ={'':''}
    
    return render_to_response(template, params, context_instance=RequestContext(request))
    

def deleteCourse(request):
    
    config = ConfigParser.ConfigParser()
    config.read('moo.ini')
				
    host = config.get("bottle","host")
    port = config.get("bottle","port")
	
    template = 'welcome.html'
    params = {'':''}
	
    if request.method == 'POST':
	
	print 'Deletecourse.'	
	courseid = request.POST['courseid']
	if len(courseid) > 0:
	    args = {'id':courseid}
	    encoded_args = urllib.urlencode(args)
	    url='http://'+host+':'+port+'/course/id?' + encoded_args
	    print 'search course URL: ',url
	    method = 'DELETE'
	    request = urllib2.Request(url,'')
	    request.get_method = lambda: method
		    
	    try: 
		response = urllib2.urlopen(request)
		r=response.read()	
		result =json.loads(r)
		
		print result
		params = {'result':'Course is deleted successfully.'}
		template = 'welcome.html'
				    
	    except urllib2.HTTPError, e:
		if(e.code == 400):				 
		    template = 'welcome.html'
		    params = {'result':'ID is invalid.'}
		elif(e.code == 404):
		    template = 'welcome.html'
		    params = {'result':'Course not found.'}
		elif(e.code == 500):
		    template = 'welcome.html'
		    params = {'result':'Server error, try again later.'}		
	else:
	    template = 'course/courseDeleteForm.html'
	    params = {'result':'Enter course id!'}

    return render_to_response(template, params, context_instance=RequestContext(request))
def displayAnnouncementForm(request): 
    template = 'announcement/announcement.html'
    params ={'':''}
    return render_to_response(template, params, context_instance=RequestContext(request))

def addAnnouncement(request):
    config = ConfigParser.ConfigParser()
    config.read('moo.ini')
				
    host = config.get("bottle","host")
    port = config.get("bottle","port")
	
    template = 'welcome.html'
    params = {'':''}
	
    if request.method == 'POST':
	form = AnnouncementForm(request.POST)		
		
	if form.is_valid():
	    	
	    addupdatestatus = request.POST['addupdatestatus']
	    courseid = request.POST['courseid']
	    title = request.POST['title']
	    description= request.POST['description']
	    postDate = request.POST['postDate']
	    #attachment = request.POST['attachment']	
	    status = request.POST['status']	
	
	    #new course -courseid = 0
	    #update course - courseid !=0
	    
	    if addupdatestatus =='0':
		url='http://'+host+':'+port+'/announcement'
		method = 'POST'
	    else:
		args = {'id':courseid}
		encoded_args = urllib.urlencode(args)
		url='http://'+host+':'+port+'/announcement/update/id?' + encoded_args
		method = 'PUT'			

	    args = {'courseid':courseid,'title':title,'description':description,'postDate':postDate,'status':status}

	    encoded_args = urllib.urlencode(args)
	    request = urllib2.Request(url,encoded_args)
	    request.get_method = lambda: method
			   
			
	    try: 
		response = urllib2.urlopen(request)	
		r=response.read()
		template = 'welcome.html'
		result=json.loads(r)
		cid = result['id']
		
		params = {'result':'Announcement is added/updated succesfully! Announcement id:'+cid}
					
	    except urllib2.HTTPError, e:
		template = 'announcement/announcement.html'
		params = {'result':'Server error, try later'}
		
	else:
	    print 'Invalid form entered. Populate data on form.'
	    courseid = request.POST['courseid']
	    title = request.POST['title']
	    description = request.POST['description']
	    postDate = request.POST['postDate']
	    status = request.POST['status']
	    
	    params = {'courseid':courseid,'title':title,'description':description,'postDate':postDate,'status':status}
	    template = 'announcement/announcement.html'
				   
    return render_to_response(template, params, context_instance=RequestContext(request)) 
  		
def displayAnnouncementSearchForm(request):
    template = 'announcement/announcementSearchForm.html'
    params ={'':''}
       
    return render_to_response(template, params, context_instance=RequestContext(request))   

def searchAnnouncement(request):
    config = ConfigParser.ConfigParser()
    config.read('moo.ini')
				
    host = config.get("bottle","host")
    port = config.get("bottle","port")
	
    template = 'welcome.html'
    params = {'':''}
	
    if request.method == 'POST':
	
	print 'Search announcement.'	
	courseid = request.POST['courseid']
	if len(courseid) > 0:
	    args = {'id':courseid}
	    encoded_args = urllib.urlencode(args)
	    url='http://'+host+':'+port+'/announcement/id?' + encoded_args
	    print 'search course URL: ',url
	    method = 'GET'
	    request = urllib2.Request(url,'')
	    request.get_method = lambda: method
		    
	    try: 
		response = urllib2.urlopen(request)	
		r=response.read()
		result =json.loads(r)
		print 'result',result

		courseid=result['courseid']
		title= result['title']
		description=result['description']
		postDate=result['postDate']		
		status=result['status']
		
		
	
		params = {'result': 'Record Found!!','courseid':courseid,'title':title,'description':description,'postDate':postDate,'status':status}
		template = 'announcement/displayAnnouncement.html'
				    
	    except urllib2.HTTPError, e:
		if(e.code == 400):				 
		    template = 'welcome.html'
		    params = {'result':'ID is invalid.'}
		elif(e.code == 404):
		    template = 'welcome.html'
		    params = {'result':'Course not found.'}
		elif(e.code == 500):
		    template = 'welcome.html'
		    params = {'result':'Server error, try again later.'}		
	else:
	    template = 'announcement/announcementSearchForm.html'
	    params = {'result':'Enter course id!'}

    return render_to_response(template, params, context_instance=RequestContext(request))
    

def listAnnouncement(request):  
    config = ConfigParser.ConfigParser()
    config.read('moo.ini')
				   
    host = config.get("bottle","host")
    port = config.get("bottle","port")
    template = 'welcome.html'
    params = {'':''}

    url='http://'+host+':'+port+'/announcement/list'
    print 'list category URL: ',url
    method = 'GET'
    request = urllib2.Request(url,'')
    request.get_method = lambda: method
			
    try: 
	response = urllib2.urlopen(request)	
	c = response.read()
        clist=json.loads(c)
        print clist
	Announcement_list=[]
	for row in clist:
	    id_list=row
	    aid=id_list['_id']
	   # instr=id_list['instructor']

	    Announcement_list+=[{"id":aid['$oid'], "title": id_list['title'],"description": id_list['description'],"postDate": id_list['postDate'],"status": id_list['status'], "courseid":id_list['courseid']}]
    
	template='announcement/viewAnnouncementList.html'
	AnnouncementList= Announcement_list
	params={'AnnouncementList':AnnouncementList}	
	
    except urllib2.HTTPError, e:
	if(e.code == 500):				 
	    template = 'welcome.html'
	    params = {'result':'Server error, try again later.'}	   
	
    return render_to_response(template, params, context_instance=RequestContext(request))
     


def displayAnnouncementDeleteForm(request):
    template = 'announcement/announcementDeleteForm.html'
    params ={'':''}
    
    return render_to_response(template, params, context_instance=RequestContext(request))   

def deleteAnnouncement(request):
    
    config = ConfigParser.ConfigParser()
    config.read('moo.ini')
				
    host = config.get("bottle","host")
    port = config.get("bottle","port")
	
    template = 'welcome.html'
    params = {'':''}
	
    if request.method == 'POST':
	
	print 'DeleteAnnouncement.'	
	courseid = request.POST['courseid']
	if len(courseid) > 0:
	    args = {'id':courseid}
	    encoded_args = urllib.urlencode(args)
	    url='http://'+host+':'+port+'/announcement/id?' + encoded_args
	    print 'search announcement URL: ',url
	    method = 'DELETE'
	    request = urllib2.Request(url,'')
	    request.get_method = lambda: method
		    
	    try: 
		response = urllib2.urlopen(request)
		r=response.read()	
		result =json.loads(r)
		
		print result
		params = {'result':'Announcement is deleted successfully.'}
		template = 'welcome.html'
				    
	    except urllib2.HTTPError, e:
		if(e.code == 400):				 
		    template = 'welcome.html'
		    params = {'result':'ID is invalid.'}
		elif(e.code == 404):
		    template = 'welcome.html'
		    params = {'result':'Announcement not found.'}
		elif(e.code == 500):
		    template = 'welcome.html'
		    params = {'result':'Server error, try again later.'}		
	else:
	    template = 'announcement/announcementDeleteForm.html'
	    params = {'result':'Enter course id!'}

    return render_to_response(template, params, context_instance=RequestContext(request))
  		

    
  		
def logout_view(request):
    
    template = 'login.html'                
    logout(request)
    
    return render_to_response(template, '', context_instance=RequestContext(request))
    
