from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^$", views.su_login, name="su-login"),
    url(r"^logout$", views.su_logout, name="su-logout"),
]
