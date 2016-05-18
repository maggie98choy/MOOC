from django import forms

class CategoryForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(required = False)
    
class CourseForm(forms.Form):
    courseid = forms.CharField(required = False)
    categoryid = forms.CharField()
    title = forms.CharField()
    section = forms.CharField()
    department = forms.CharField(required = False)
    term = forms.CharField(required = False)   
    year = forms.CharField(required = False)
    instructorname = forms.CharField(required = False)    
    instructoremail = forms.CharField(required = False)
    hours = forms.CharField(required = False)
    description = forms.CharField(required = False)    
    hours = forms.CharField(required = False)
    version = forms.CharField(required = False)
  
class AnnouncementForm(forms.Form):
    addupdatestatus = forms.CharField(required = False)
    courseid = forms.CharField(required = False)
    title = forms.CharField()
    description = forms.CharField(required = False)    
    postDate = forms.CharField(required = False)
    status = forms.CharField(required = False)

   
   
