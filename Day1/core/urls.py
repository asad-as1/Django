from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),                # template home
    path("blogs/", views.blogs, name="blogs_api"),     # API: list/create
    path("blogs/<int:blog_id>/", views.blog_detail, name="blog_detail_api"),  # API: detail/update/delete
]
