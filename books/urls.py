from django.conf.urls import patterns, include, url
from book_search import views
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

    #views
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.logreg ,name="logreg"),
    url(r'^login/', views.logreg ,name="logreg"),
    url(r'^results/', views.results, name="results"),
    url(r'^search/', views.search, name="search"),
    url(r'^home/', views.home, name="home"),
    url(r'^add_book_page/', views.add_book_page, name="add_book_page"),

    #functions
    url(r'^register/', views.register, name="register"),
    url(r'^loger/', views.loger, name="loger"),
    url(r'^logout/', views.log_out, name="log_out"),
    url(r'^add_book/', views.add_book, name="add_book"),
    url(r'^get_account/', views.get_account, name="get_account"),
    url(r'^autocompletetitle/', views.autocompletetitle, name="autocompletet"),
    url(r'^autocompleteauthor/', views.autocompleteauthor, name="autocompletea"),
    url(r'^autocompletepublisher/', views.autocompletepublisher, name="autocompletep"),
    url(r'^delete/', views.delete_book, name="delete"),
)
