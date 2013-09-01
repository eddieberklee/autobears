from django.conf.urls import patterns, include, url

urlpatterns = patterns('scrape.views',
    url(r'^$', 'index', name='index'),
    # url(r'^add_quote/$', 'app.views.add_quote', name='add_quote'),
