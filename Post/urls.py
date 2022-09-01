from django.urls import path

from .views import blogFilter, blogs, categories, create, delete, edit, index, likepost, profile, searchBlog, yourBlog, single

urlpatterns = [
    path('index/', index, name='index'),
    path('blog/', blogs, name='blogs'),
    path('category/<int:id>', blogFilter, name='blogfilter'),
    path('categories/', categories, name='categories'),
    path('single/<int:id>', single, name='single'),
    path('create/', create, name='create'),
    path('edit/<int:id>', edit, name='edit'),
    path('delete/<int:id>', delete, name='delete'),
    path('yourblog/', yourBlog, name='yourblog'),
    path('profile/<int:id>',profile, name='profile'),
    path('search/',searchBlog, name='search'),
    path('like/<int:id>',likepost, name='likepost'),
]