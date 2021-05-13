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
        path('pages-users.html', views.userController, name='userController'),
        path('pages-category.html', views.categoryController, name='categoryController'),
        path('page.html', views.page, name='page'),
        path('post/<int:post_id>.html', views.post, name='post'),
        path('register.html', views.register, name='register'),
        path('search.html', views.search, name='search'),
        path('addPost.html',views.addPost, name='addPost'),
        path('editPost/<int:post_id>.html', views.editPost, name='editPost'),
        path('deletePost/<int:post_id>.html', views.deletePost, name='deletePost'),   
        path('addUser.html',views.addUser, name='addUser'),
        path('editUser/<int:account_id>.html', views.editUser, name='editUser'),
        path('deleteUser/<int:account_id>.html', views.deleteUser, name='deleteUser'),   
        path('addCategory.html',views.addCategory, name='addCategory'),
        path('editCategory/<int:category_id>.html', views.editCategory, name='editCategory'),
        path('deleteCategory/<int:category_id>.html', views.deleteCategory, name='deleteCategory'),   
]
