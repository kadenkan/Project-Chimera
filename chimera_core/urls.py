from django.urls import include, path
from . import views

app_name = 'chimera-core'

urlpatterns == [
    path(r'^captcha/', include('captcha.urls')),
]