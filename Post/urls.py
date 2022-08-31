from django.urls import path

from .views import blogFilter, blogs, categories, create, delete, edit, index, yourBlog, single

urlpatterns = [
    path('index/', index, name='index'),
    path('blog/', blogs, name='blogs'),
    path('blog/<int:id>', blogFilter, name='blogfilter'),
    path('categories/', categories, name='categories'),
    path('single/<int:id>', single, name='single'),
    path('create/', create, name='create'),
    path('edit/<int:id>', edit, name='edit'),
    path('delete/<int:id>', delete, name='delete'),
    path('yourblog/', yourBlog, name='yourblog'),
]