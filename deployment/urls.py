from django.conf.urls import url
from deployment.views.ProjectView import ProjectListView
from deployment.views.ProjectView import ProjectAddView
from deployment.views.ProjectView import ProjectUpdateView
from deployment.views.ProjectView import ProjectDeleteView
from deployment.views.ProjectView import ProjectSearchView
from deployment.views.TicketView import TicketListView
from deployment.views.TicketView import TicketAddView
from deployment.views.TicketView import TicketDetailView
from deployment.views.TicketView import TicketSqlAndConfigView
from deployment.views.TicketView import TicketSuccess

urlpatterns = [
    url(r'^project/list/$',ProjectListView.as_view(),name='project_list'),
    url(r'^project/add/$',ProjectAddView.as_view(),name='project_add'),
    url(r'^project/update/(?P<id>[0-9]+)/$',ProjectUpdateView.as_view(),name='project_update'),
    url(r'^project/delete/$',ProjectDeleteView.as_view(),name='project_delete'),
    url(r'^project/search/$',ProjectSearchView.as_view(),name='project_search'),
    url(r'^ticket/list/$',TicketListView.as_view(),name="ticket_list"),
    url(r'^ticket/add/$',TicketAddView.as_view(),name='ticket_add'),
    url(r'^ticket/detail/$',TicketDetailView.as_view(),name='ticket_detail'),
    url(r'^ticket/sql_and_config/$',TicketSqlAndConfigView.as_view(),name='ticket_sql_config'),
    url(r'^ticket/success/$',TicketSuccess.as_view(),name="ticket_success")
]