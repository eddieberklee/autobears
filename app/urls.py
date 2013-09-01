from django.conf.urls import patterns, include, url

urlpatterns = patterns('app.views',
    url(r'^$', 'index', name='index'),
    # url(r'^add_quote/$', 'add_quote', name='add_quote'),
