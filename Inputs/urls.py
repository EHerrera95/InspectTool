from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.home, name='home'),
    path("inputsCures/", views.inputsCures, name='inputCures'),
    path("inputs/", views.inputs, name="inputs"),
    path("results/", views.results, name="results"),
    path("resultsCures/", views.resultsCures, name="resultsCures"),
    # path("changes/", views.changes, name="changes"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),    
    # path("register/", views.registerPage, name="register")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    