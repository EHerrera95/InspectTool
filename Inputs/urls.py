from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

#edits 2

urlpatterns = [
    path("", views.inputs, name="inputs"),
    path("results/", views.results, name="results")
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    