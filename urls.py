from django.conf.urls.defaults import *
from elephantblog.models import Entry
from django.template import RequestContext
from feincms.translations import short_language_code
from django.conf import settings


entry_dict = {
    'queryset': Entry.objects.active().filter(language=short_language_code),
    'paginate_by' : 3
    }

urlpatterns = patterns('',
    url(r'^category/(?P<category>[^/]+)/$', 'elephantblog.views.category_object_list', entry_dict, name='elephantblog_category'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[^/]+)/$', 'elephantblog.views.blog_detail', 
        entry_dict, name='elephantblog_entry_detail'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'elephantblog.views.archive_day', entry_dict, name='elephantblog_day'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'elephantblog.views.archive_month', entry_dict, name='elephantblog_month'),
    url(r'^(?P<year>\d{4})/$', 'elephantblog.views.archive_year', entry_dict, name='elephantblog_year'),
    url(r'^$', 'django.views.generic.list_detail.object_list', dict(entry_dict, **{ 'template_name':'entry_list.html'}), name='elephantblog_all' ),
    
    

)

if 'tagging' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',url(r'^tag/(?P<tag>[^/]+)/$', 'tagging.views.tagged_object_list', 
        { 'template_name':'entry_list_tagged.html', 'queryset_or_model': entry_dict['queryset'], 'paginate_by':entry_dict['paginate_by']}, name='elephantblog_tag'),)



"""
    url(r'^blog/alle-eintrage/$', 'django.views.generic.simple.redirect_to', {'url':'1/'}),
    url(r'^blog/alle-eintrage/(?P<page>[0-9]+)/$', 'feincms.views.generic.list_detail.object_list', dict(entry_dict, paginate_by=5)),

    url(r'^blog/tag/(?P<tag>[^/]+)/$', 'django.views.generic.simple.redirect_to', {'url':'1/'}, name='get_entries_by_tag'),
    url(r'^blog/tag/(?P<tag>[^/]+)/(?P<page>[0-9]+)/$', 'elephantblog.views.blog_entries_by_tag', entry_dict),

    url(r'^blog/(?P<year>\d{4})/(?P<month>\d{2})/$', 'django.views.generic.simple.redirect_to', {'url':'1/'}, name='get_entries_by_month'),
    url(r'^blog/(?P<year>\d{4})/(?P<month>\d{2})/(?P<page>[0-9]+)/$', 'elephantblog.views.blog_entries_by_month', entry_dict),

    url(r'^blog/(?P<category>[^/]+)/$', 'django.views.generic.simple.redirect_to', {'url':'1/'}, name='get_entries_by_cat'),
    url(r'^blog/(?P<category>[^/]+)/(?P<page>[0-9]+)/$', 'elephantblog.views.blog_entries_by_cat', entry_dict),
"""