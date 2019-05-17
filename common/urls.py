from django.conf.urls import url
from common.views import index,LogoutView,user_exists,password_check

urlpatterns = [
    url(r'^$',index,name='index'),
    url(r'^logout/$',LogoutView.as_view(),name='logout'),
    url(r'^user/exists/$',user_exists,name='user_exists'),
    url(r'^check/password/$',password_check,name='password_check')
]