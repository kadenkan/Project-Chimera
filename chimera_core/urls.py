from django.conf.urls import url,include
from chimera_core import views

app_name = 'chimera_core'

urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^login_form/$',views.login_form,name='login_form'),
    url(r'^user_login/$',views.user_login,name='user_login'),
]