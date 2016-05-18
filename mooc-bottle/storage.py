from pymongo import Connection
from bson.json_util import dumps
from bson.objectid import ObjectId

connection= Connection('localhost',27017)
db= connection.mooc1
user=db.usercollection
category= db.categorycollection
course=db.coursecollection
announcement= db.announcementcollection
quiz=db.quizcollection
discussion=db.Discussion
message=db.Message

def addcategory(categories):
	category.insert(categories)
	return 1


def addcourse(courses):
	course.insert(courses)
	return 1

def listcategory():
	c=category.find()
	return dumps(c)
	
def listcourse():
	c=course.find()
	return dumps(c)

def getcourse(cid):
	c=course.find_one({"_id":ObjectId(cid)})
	if c is None:
		return 0
	else:
		return dumps(c)

def getcategory(cid):
	c=category.find_one({"_id":ObjectId(cid)})
	if c is None:
		return 0
	else:
		return dumps(c)

def updatecourse(cid,courses):

	c=course.find_one({"_id":ObjectId(cid)})
	if c is None:
		return 0
	else:
		course.update({'_id':ObjectId(cid)},{"$set":{'category':courses['category'],'title':courses['title'],'section':courses['section'],'dept':courses['dept'], 'term':courses['term'], 'year': courses['year'], 'instructor':courses['instructor'],'days':courses['days'],'hours':courses['hours'],'Description':courses['Description'],'attachment':courses['attachment'],'version':courses['version']}})
		#course.update({'_id':ObjectId(cid)},{"$set":{'category':courses['category']}})
		co=course.find_one({"_id":ObjectId(cid)})
		print co
		return dumps(co)

def deletecourse(cid):
	c=course.find_one({"_id":ObjectId(cid)})
	if c is None:
		return 0
	else:
		course.remove({'_id':ObjectId(cid)})
		return 1

def enrollcourse(cid,uid):
	email=uid
	own=""
	
	quizzes=""
	
	exiting_email=user.find_one({"email":email})
	print exiting_email

	enroll=course.find_one({"_id":ObjectId(cid)})
	enrolled=enroll['title']
	
	if(exiting_email is None):
		user.insert({"email":email,"own":own,"enrolled":enrolled,"quizzes":quizzes})

	else:
		if(exiting_email['enrolled']== enrolled):
			print "hello"
		elif(exiting_email['enrolled']==[]):
			user.update({"email":email},{"$set":{"enrolled":enrolled}})

		else:
			new_enroll=[exiting_email['enrolled'],enrolled]
			print new_enroll
			user.update({"email":email},{"$set":{"enrolled":new_enroll}})

	return 1
	
def unenrollcourse(cid,uid):
	email=uid
	own=""
	quizzes=""

	exiting_course=user.find_one({"email":email})
	unen= course.find_one({"_id":ObjectId(cid)})
	unenroll=unen['title']
	if(exiting_course['enrolled'] == unenroll):
		print "hello"
		user.update({"email":email},{"$set":{"enrolled":""}})
	else:
		print "hii"
		user.update({"email":email},{"$pull":{"enrolled":unenroll}})
	return 1

def addannouncement(announcements):
	announcement.insert(announcements)
	return 1

def listannouncement():
	c=announcement.find()
	return dumps(c)

def getannouncement(aid):
	c=announcement.find_one({"courseid":aid})
	if c is None:
		return 0
	else:
		return dumps(c)
def updateannouncement(aid,announcements):

	c=announcement.find_one({"courseid":aid})
	print 'c = ',c
	if c is None:
		return 0
	else:
		announcement.update({'_id':ObjectId(c['_id'])},{"$set":{'courseid':announcements['courseid'],'title':announcements['title'],'description':announcements['description'],'postDate':announcements['postDate'],'status':announcements['status']}})
		#course.update({'_id':ObjectId(cid)},{"$set":{'category':courses['category']}})
		co=announcement.find_one({"courseid":aid})
		print co
		return dumps(co)

def deleteannouncement(aid):
	c=announcement.find_one({"courseid":aid})
	if c is None:
		return 0
	else:
		announcement.remove({"courseid":aid})
		return 1






