from django.conf.urls import url
from job.views.JobView import JobAddView
from job.views.JobView import JobListView
from job.views.JobView import JobUpdateView
from job.views.JobResultView import JobExecuteView
from job.views.JobResultView import JobResultView
from job.views.JobHistoryView import JobHistoryList
from job.views.JobHistoryView import JobHistoryResultView
from job.views.JobView import JobDeleteView

urlpatterns = [
    url(r'^execute/(?P<id>[0-9]+)/$', JobExecuteView.as_view(), name='job_execute'),
    url(r'^ansible-playbook/$', JobExecuteView.as_view(), name='ansible_playbook'),
    url(r'^result/$', JobResultView.as_view(), name='job_result'),
    url(r'^content/$', JobAddView.as_view(), name='job_content'),
    url(r'^list/$', JobListView.as_view(), name='job_list'),
    url(r'^delete/$', JobDeleteView.as_view(), name='job_delete'),
    url(r'^update/(?P<id>[0-9]+)/$', JobUpdateView.as_view(),name='job_update'),
    url(r'^history/$', JobHistoryList.as_view(), name='job_history'),
    url(r'^history/result/(?P<jobid>(.*))/$', JobHistoryResultView.as_view(), name='job_history_result')
]