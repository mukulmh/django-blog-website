from django.urls import path

from .views import blogFilter, blogs, categories, createPost, deletePost, deleteComment, editPost, editComment, index, likepost, authorProfile, searchBlog, setting, yourBlog, singlePost

urlpatterns = [
    path('', index, name='index'),
    path('blogs/', blogs, name='blogs'),
    path('category/<int:id>', blogFilter, name='blogfilter'),
    path('categories/', categories, name='categories'),
    path('blog/<int:id>', singlePost, name='single'),
    path('writepost/', createPost, name='createPost'),
    path('editpost/<int:id>', editPost, name='editPost'),
    path('deletepost/<int:id>', deletePost, name='deletePost'),
    path('yourblog/', yourBlog, name='yourblog'),
    path('author/<int:id>',authorProfile, name='author'),
    path('search/',searchBlog, name='search'),
    path('profile/',setting, name='setting'),
    path('like/<int:id>',likepost, name='likepost'),
    path('deleteComment/<int:id>',deleteComment, name='deleteComment'),
    path('editComment/<int:id>',editComment, name='editComment'),
]