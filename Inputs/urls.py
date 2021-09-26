from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.home, name='home'),
    path("inputs/", views.inputs, name="inputs"),
    path("results/", views.results, name="results"),
    path("instructions/", views.instructions, name="instructions"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),    
    path("register/", views.registerPage, name="register")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    