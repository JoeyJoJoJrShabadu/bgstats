from django.conf.urls import patterns, include, url

from rest_framework.urlpatterns import format_suffix_patterns

from bgstatsdb import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('bgstatsdb.views',
    # Examples:
    # url(r'^$', 'bgstats.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^bg/$', 'api_root'),
    url(r'^bg/gameinstance/$', views.GameInstanceList.as_view(), name='gameinstance-list'),
    url(r'^bg/gameinstance/(?P<pk>[0-9]+)/$', views.GameInstanceDetail.as_view(), name='gameinstance-detail'),
)

for key, val in views.AUTOMODELS.items():
    urlpatterns.append(url(r'^bg/' + key + '/$',
                           getattr(views, val[0] + 'List').as_view(),
                           name=key + '-list'))
    urlpatterns.append(url(r'^bg/' + key + '/(?P<pk>[0-9]+)/$',
                           getattr(views, val[0] + 'Detail').as_view(),
                           name=key + '-detail'))
    
urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += patterns('', url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')))