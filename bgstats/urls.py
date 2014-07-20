from django.conf.urls import patterns, include, url

from rest_framework.urlpatterns import format_suffix_patterns

from bgstatsdb import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bgstats.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

for key, val in views.ALLMODELS.items():
    urlpatterns.append(url(r'^bg/' + key + '/$', getattr(views, val[0] + 'List').as_view()))
    urlpatterns.append(url(r'^bg/' + key + '/(?P<pk>[0-9]+)/$', getattr(views, val[0] + 'Detail').as_view()))
    
urlpatterns = format_suffix_patterns(urlpatterns)