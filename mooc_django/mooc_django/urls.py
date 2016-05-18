from django.conf.urls import patterns, include, url
from django.contrib import admin

from views import login, logout_view, displayCategoryForm, addCategory, displayCategorySearchForm,searchCategory, listCategory, displayCourseForm, addCourse,displayCourseSearchForm,searchCourse,listCourse,deleteCourse,displayCourseDeleteForm, displayEnrollForm, enrollCourse, displayDropForm, dropCourse, addAnnouncement, deleteAnnouncement , displayAnnouncementForm, displayAnnouncementSearchForm, listAnnouncement, displayAnnouncementDeleteForm, searchAnnouncement

import settings

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),    
    url(r'^$', login),	
    url(r'^login/$', login),	
    url(r'^logout/$', logout_view),
    url(r'^category/displayForm/$', displayCategoryForm),
    url(r'^category/categorySearchForm/$', displayCategorySearchForm),
    url(r'^category/search/$', searchCategory),
    url(r'^category/add/$', addCategory),
    url(r'^category/list/$', listCategory),
    
    url(r'^course/displayForm/$', displayCourseForm),
    url(r'^course/add/$', addCourse),
    url(r'^course/courseSearchForm/$', displayCourseSearchForm),
    url(r'^course/search/$', searchCourse),
    url(r'^course/update/$', addCourse),
    url(r'^course/list/$', listCourse),   
    url(r'^course/courseDeleteForm/$', displayCourseDeleteForm),
    url(r'^course/delete/$', deleteCourse),
    url(r'^course/displayEnrollForm/$', displayEnrollForm),
    url(r'^course/displayDropForm/$', displayDropForm),
    url(r'^course/enroll/$', enrollCourse),
    url(r'^course/drop/$', dropCourse),    

    url(r'^announcement/displayForm/$', displayAnnouncementForm),
    url(r'^announcement/add/$', addAnnouncement),
    url(r'^announcement/announcementSearchForm/$', displayAnnouncementSearchForm),
    url(r'^announcement/search/$', searchAnnouncement),
    url(r'^announcement/update/$', addAnnouncement),
    url(r'^announcement/list/$', listAnnouncement),   
    url(r'^announcement/announcementDeleteForm/$', displayAnnouncementDeleteForm),
    url(r'^announcement/delete/$', deleteAnnouncement),
    
    
  
    
    
    
   
)


