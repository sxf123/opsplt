from django.conf.urls import url
from database.views.DatabaseView import DatabaseListView
from database.views.DatabaseView import DatabaseAddView
from database.views.DatabaseView import DatabaseUpdateView
from database.views.DatabaseView import DatabaseDeleteView
from database.views.DatabaseView import DatabaseSearchView

urlpatterns = [
    url(r'^list/$',DatabaseListView.as_view(),name='database_list'),
    url(r'^add/$',DatabaseAddView.as_view(),name='database_add'),
    url(r'^update/(?P<id>[0-9]+)/$',DatabaseUpdateView.as_view(),name='database_update'),
    url(r'^delete/$',DatabaseDeleteView.as_view(),name='database_delete'),
    url(r'^search/$',DatabaseSearchView.as_view(),name='database_search')
]