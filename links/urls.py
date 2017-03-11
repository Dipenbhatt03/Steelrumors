from django.conf.urls import  url
import views
from django.contrib.auth.views import login,logout_then_login
from django.contrib.auth.decorators import login_required
urlpatterns=[
    url(r'^$', views.LinkListView.as_view(), name='home'),
    url(r'^login/$',login,{'template_name':"login.html"},name='login'),
    url(r'^logout/$',logout_then_login,name='logout'),
    url(r'^users/(?P<slug>\w+)/$',login_required(views.UserProfileDetailView.as_view()),name='profile'),
    url(r'^edit_profile/$',login_required(views.UserProfileEditView.as_view()),name='edit_profile'),#login_required is used here so only if the user
    # is logged in ,then only should he be able to access this link
    url(r'^link/create/$',login_required(views.LinkCreateView.as_view()),name='link_create'),
    url(r'^link/(?P<pk>\d+)/$',views.LinkDetailView.as_view(),name='link_detail'),
    url(r'^link/update/(?P<pk>\d+)/$',login_required(views.LinkUpdateView.as_view()),name='link_update'),
    url(r'^link/delete/(?P<pk>\d+)/$',login_required(views.LinkDeleteView.as_view()),name='link_delete'),
    url(r'^vote/$',login_required(views.VoteFormView.as_view()),name='vote'),
]