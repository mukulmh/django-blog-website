from django.urls import path

from .views import blogs, categories, create, delete, edit, index, profile, single

urlpatterns = [
    path('index/', index, name='index'),
    path('blog/', blogs, name='blogs'),
    path('categories/', categories, name='categories'),
    path('single/<int:id>', single, name='single'),
    path('create/', create, name='create'),
    path('edit/<int:id>', edit, name='edit'),
    path('delete/<int:id>', delete, name='delete'),
    path('profile/', profile, name='profile'),
]