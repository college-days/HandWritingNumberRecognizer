from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
import views
import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'recogNumberServer.views.home', name='home'),
    # url(r'^recogNumberServer/', include('recogNumberServer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.root),
    url(r'^index/$', views.index),
    url(r'^upload/$', views.getImage),
    url(r'^process/$', views.processImage),
    url(r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.IMAGEPATH}),
    url(r'^styles/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.CSSPATH}),
)
