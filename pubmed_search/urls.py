from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView, DetailView
from pubmed_search.models import Article

urlpatterns = patterns('',
    url(r'^autosearch/', 'pubmed_search.views.autosearch', name='autosearch'),
    url(r'^article/(?P<pk>\d+)/$',
        DetailView.as_view(model=Article),
        name='article_detail'),
    url(r'^articles/$', ListView.as_view(model=Article), name='article_list'),
    url(r'^$', 'pubmed_search.views.search', name='search'),
)
