from django.urls import path

from app.post import views

urlpatterns = [
    path ('blog_post/', views.blog_post, name='blog_post'),
    path ('display_post/', views.display_post, name='display_post'),
    path ('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path ('update_post/', views.update_post, name='update_post')
]
