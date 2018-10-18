from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url('^$', views.home, name='home'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^edit/', views.edit, name='edit'),
    url(r'^upload_image/', views.upload, name='upload'),
    url(r'^search/', views.search_results, name='search'),
    url(r'^review/(?P<project_id>\d+)$', views.review, name='review'),
    
    # url(r'^comment/(?P<pk>\d+)',views.new_comment,name='comment'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
