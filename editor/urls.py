from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("privacy/", views.privacy, name="privacy"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("blog/photo-20kb/", views.blog1),
path("blog/jpg-to-png/", views.blog2),
path("blog/compress-image/", views.blog3),
]
from django.http import HttpResponse

def ads_txt(request):
    return HttpResponse("google.com, pub-789203977629393, DIRECT, f08c47fec0942fa0")

urlpatterns += [
    path("ads.txt", ads_txt),
]