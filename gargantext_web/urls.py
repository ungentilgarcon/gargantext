from django.conf.urls import patterns, include, url

from django.contrib import admin

from gargantext_web.views import home, projects, project, corpus
from gargantext_web.views import delete_project, delete_corpus
from gargantext_web.views import exploration
from gargantext_web.views import explorer_graph, explorer_matrix

admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'gargantext_web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    
    url(r'^$', home),
    
    url(r'^projects/$', projects),
    url(r'^project/(\d+)/delete/$', delete_project),
    
    url(r'^project/(\d+)/$', project),
    
    url(r'^project/(\d+)/corpus/(\d+)/$', corpus),
    url(r'^project/(\d+)/corpus/(\d+)/delete/$', delete_corpus),
    
    url(r'^graph$', explorer_graph),
    url(r'^matrix$', explorer_matrix),
    
    url(r'^exploration$', exploration),
)

from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
)

