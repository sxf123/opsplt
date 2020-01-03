from django.conf.urls import url
from database.views.DatabaseView import DatabaseListView
from database.views.DatabaseView import DatabaseAddView
from database.views.DatabaseView import DatabaseUpdateView
from database.views.DatabaseView import DatabaseDeleteView
from database.views.DatabaseView import DatabaseSearchView
from database.views.SqlFileView import SqlFileAddView
from database.views.SqlFileView import SqlFileListView
from database.views.SqlFileView import SqlFileUpdateView
from database.views.SqlFileView import SqlFileDeleteView
from database.views.SqlFileView import SqlFileExistView
from database.views.SqlFileView import SqlFileVisitView
from database.views.DbMigrateView import MigrateView
from database.views.DbMigrateView import MigrateStatusView
from database.views.DbMigrateView import MigrateResultView

urlpatterns = [
    url(r'^list/$',DatabaseListView.as_view(),name='database_list'),
    url(r'^add/$',DatabaseAddView.as_view(),name='database_add'),
    url(r'^update/(?P<id>[0-9]+)/$',DatabaseUpdateView.as_view(),name='database_update'),
    url(r'^delete/$',DatabaseDeleteView.as_view(),name='database_delete'),
    url(r'^search/$',DatabaseSearchView.as_view(),name='database_search'),
    url(r'^sql/add/(?P<id>[0-9]+)/$',SqlFileAddView.as_view(),name='sql_add'),
    url(r'^sql/list/(?P<id>[0-9]+)/$',SqlFileListView.as_view(),name='sql_list'),
    url(r'^sql/update/(?P<id>[0-9]+)/$',SqlFileUpdateView.as_view(),name='sql_update'),
    url(r'^sql/delete/$',SqlFileDeleteView.as_view(),name='sql_delete'),
    url(r'^sql/exist/$',SqlFileExistView.as_view(),name='sql_exist'),
    url(r'^sql/visit/(?P<id>[0-9]+)/$',SqlFileVisitView.as_view(),name='sql_visit'),
    url(r'^migrate/$',MigrateView.as_view(),name='db_migrate'),
    url(r'^migrate/status/$',MigrateStatusView.as_view(),name='db_migrate_status'),
    url(r'^migrate/result/$',MigrateResultView.as_view(),name='db_migrate_result')
]