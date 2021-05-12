from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
        path('index.html', views.index, name='index'),
        path('contact.html', views.contact, name='contact'),
        path('category/<int:id_category>.html', views.category, name='category'),
        path('login.html', views.login, name='login'),
        path('logout.html', views.logout, name='logout'),
        path('admin.html', views.admin, name='admin'),
        path('pages-post.html', views.newsController, name='newsController'),
        path('page.html', views.page, name='page'),
        path('post/<int:post_id>.html', views.post, name='post'),
        path('register.html', views.register, name='register'),
        path('search.html', views.search, name='search'),
        path('addPost.html',views.addPost, name='addPost'),
        path('editPost/<int:post_id>.html', views.editPost, name='editPost'),
        path('deletePost/<int:post_id>.html', views.deletePost, name='deletePost')        
]
