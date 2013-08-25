from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django.contrib.auth.views import login, logout



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CSM.views.home', name='home'),
    # url(r'^CSM/', include('CSM.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^',include('mysite.apps.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
    (r'^getCore/$','mysite.apps.views.getCore'),
    (r'^login/$',login),
    (r'^logout/$','mysite.apps.views.logout_view'),
    (r'^perfil/$','mysite.apps.views.profile_view'),
    (r'^perfil/edit/$','mysite.apps.views.edprofile_view'),
    (r'^perfil/elim/$','mysite.apps.views.elprofile_view'),
    (r'^registro/$','mysite.apps.views.register_view'),
    (r'^accounts/login/$',login),
    (r'^accounts/profile/$','mysite.apps.views.profile_view'),
)
